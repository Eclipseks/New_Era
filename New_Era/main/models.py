from django.db import models

class Upload(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    brand = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    date_registr = models.DateField(auto_now_add=False)
    date_upload = models.DateField(auto_now_add=True)
    mpc1 = models.FloatField()
    mpc2 = models.FloatField()
    mpc3 = models.FloatField()
    mpc4 = models.FloatField()
    