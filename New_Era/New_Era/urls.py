from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('home/', views.upload_list, name='upload_list'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login')
]
