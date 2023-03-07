from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UploadFileForm
import pandas as pd
from .models import Upload
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main/upload_list.html')  # замените 'home' на имя вашей главной страницы
        else:
            messages.error(request, 'Неверные имя пользователя или пароль')
    return render(request, 'main/login.html')


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
        files = Upload.objects.order_by('county')
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


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)  # для Excel
            # df = pd.read_csv(file)  # для CSV
            for index, row in df.iterrows():
                try:
                    upload = Upload(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        phone=row['phone'],
                        email=row['email'],
                        brand=row['brand'],
                        # county=row['county'],
                        date_registr=row['date_registr'],
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
