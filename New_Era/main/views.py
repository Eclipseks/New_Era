from datetime import datetime
import os

from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from .forms import UploadFileForm
import pandas as pd
from .models import Upload
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


# Autentification page
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # User.objects.create_user(username=username, email='artur.dima68@gmail.com', password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_list')  # замените 'home' на имя вашей главной страницы
        else:
            messages.error(request, 'Неверные имя пользователя или пароль')
    return render(request, 'main/login.html')


# Table on main page
@login_required()
def upload_list(request):
    # get the sorting parameter from the URL
    sort = request.GET.get('sort')

    # set the default sorting
    if sort == None or sort == 'DateUpload':
        files = Upload.objects.order_by('date_upload')
    elif sort == 'Firstname':
        files = Upload.objects.order_by('first_name')
    elif sort == 'Lastname':
        files = Upload.objects.order_by('last_name')
    elif sort == 'Email':
        files = Upload.objects.order_by('email')
    elif sort == 'Brend':
        files = Upload.objects.order_by('brand')
    elif sort == 'Country':
        files = Upload.objects.order_by('country')
    elif sort == 'DateRegistr':
        files = Upload.objects.order_by('date_registr')
    elif sort == 'Mpc1':
        files = Upload.objects.order_by('mpc1')
    elif sort == 'Mpc2':
        files = Upload.objects.order_by('mpc2')
    elif sort == 'Mpc3':
        files = Upload.objects.order_by('mpc3')
    elif sort == 'Mpc4':
        files = Upload.objects.order_by('mpc4')
    elif sort == 'Phone':
        files = Upload.objects.order_by('phone')

    return render(request, 'main/upload_list.html', {'files': files})

        

# Import data from exel, csv
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for file in files:
                # Обработка каждого файла в списке
                file_extension = os.path.splitext(file.name)[1]
                if file_extension == '.xls' or file_extension == '.xlsx':
                    df = pd.read_excel(file)
                elif file_extension == '.csv':
                    df = pd.read_csv(file)
                else:
                    continue  # Неизвестный формат файла

                for index, row in df.iterrows():
                    try:
                        try:
                            date = row['date_registr'].split(' ')
                            if len(date) == 2:
                                date_reg = date[0]
                            elif len(date) == 1:
                                date = row['date_registr']
                            else:
                                raise Exception
                        except:
                            date = '1999-11-10'
                        upload = Upload(
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            phone=row['phone'],
                            email=row['email'],
                            brand=row['brand'],
                            country=row['country'],
                            date_registr=date,
                            date_upload=datetime.now(),
                            mpc1=row['mpc1'],
                            mpc2=row['mpc2'],
                            mpc3=row['mpc3'],
                            mpc4=row['mpc4']
                        )
                        upload.save()
                    except:
                        continue

            return HttpResponseRedirect(reverse('upload_list'))
    else:
        form = UploadFileForm()
    return render(request, 'main/upload_file.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')