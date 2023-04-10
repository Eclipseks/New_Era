from datetime import datetime
import os

import openpyxl
import csv

from django.http import HttpResponse
from .forms import UploadFileForm
import pandas as pd
from django.contrib import messages
from .models import Upload
from django.db.models import Q
from dateutil.parser import parse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # replace 'home' with the name of the main page for authenticated users

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_list')  # replace 'upload_list' with the name of your desired page
        else:
            messages.error(request, 'Неверные имя пользователя или пароль')
    return render(request, 'main/login.html')


# Table on main page
@never_cache
@login_required(login_url='/login/')
def upload_list(request):
    files = Upload.objects.order_by('date_upload')

    return render(request, 'main/upload_list.html', {'files': files})

        

# Import data from exel, csv
@never_cache
@login_required(login_url='/login/')
def upload_file(request):
    duplicate_entries = []

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for file in files:
                duplicates = process_file(file)
                duplicate_entries.extend(duplicates)

            return render(request, 'main/duplicates.html', {'duplicates': duplicate_entries})
    else:
        form = UploadFileForm()
    return render(request, 'main/upload_file.html', {'form': form})


def process_file(file):
    file_extension = os.path.splitext(file.name)[1]
    if file_extension in ('.xls', '.xlsx'):
        df = pd.read_excel(file)
    elif file_extension == '.csv':
        df = pd.read_csv(file)
    else:
        return  # Unknown file format

    columns_operations = [
        ('date_registr', lambda x: parse(str(x)).strftime("%Y-%m-%d")),
        ('email', lambda x: 'example@gmail.com' if len(str(x).split('@')[1].split('.')) != 2 else x),
        ('mpc1', lambda x: 0.00 if not isinstance(x, float) else x),
        ('mpc2', lambda x: 0.00 if not isinstance(x, float) else x),
        ('mpc3', lambda x: 0.00 if not isinstance(x, float) else x),
        ('mpc4', lambda x: 0.00 if not isinstance(x, float) else x),
    ]

    upload_fields = set(field.name for field in Upload._meta.get_fields())
    
    duplicates = []

    for _, row in df.iterrows():
        upload_data = {col: op(row[col]) for col, op in columns_operations}
        upload_data.update({col: row[col] for col in row.index if col not in dict(columns_operations).keys()})
        upload_data = {col: val for col, val in upload_data.items() if col in upload_fields}

        first_name = upload_data['first_name']
        last_name = upload_data['last_name']
        phone = upload_data['phone']
        email = upload_data['email']
        brand = upload_data['brand']
        country = upload_data['country']

        is_duplicate = Upload.objects.filter(
            Q(first_name=first_name) &
            Q(last_name=last_name) &
            Q(phone=phone) &
            Q(email=email) &
            Q(brand=brand) &
            Q(country=country)
        ).exists()

        if not is_duplicate:
            upload_data['date_upload'] = datetime.now()
            upload = Upload(**upload_data)
            upload.save()
            
        if is_duplicate:
            duplicates.append(upload_data)
        else:
            upload_data['date_upload'] = datetime.now()
            upload = Upload(**upload_data)
            upload.save()

    return duplicates


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def export_view(request):
    list_hint = ['first_name', 
        'last_name', 
        'phone', 
        'email',
        'brand',
        'country',
        'date_registr',
        'date_upload',
        'mpc1',
        'mpc2',
        'mpc3',
        'mpc4'
    ]
    selected_checkboxes = request.GET.getlist('checkboxes')
    ids_str = selected_checkboxes[0].split(',')
    pqueryset = Upload.objects.filter(id__in=ids_str)

    # Increment the download counter for each exported row
    for obj in pqueryset:
        obj.download_count += 1
        obj.save()

    # Get data from the model
    rows = Upload.objects.filter(id__in=ids_str).values_list(*list_hint)

    # Get the file format from the query parameter
    file_format = request.GET.get('format', 'excel').lower()

    if file_format == 'csv':
        # Create a new CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="leed_{datetime.now().date()}.csv"'

        writer = csv.writer(response)
        headers = list_hint
        writer.writerow(headers)

        for row in rows:
            writer.writerow(row)

        return response
    else:
        # Create a new Excel file
        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        headers = list_hint
        worksheet.append(headers)

        for row_num, row in enumerate(rows, start=2):
            for col_num, value in enumerate(row, start=1):
                worksheet.cell(row=row_num, column=col_num, value=value)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="leed_{datetime.now().date()}.xlsx"'
        workbook.save(response)
        return response