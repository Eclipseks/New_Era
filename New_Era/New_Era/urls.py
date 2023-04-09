from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.upload_list, name='upload_list'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('export/', views.export_view, name='export'),
]


