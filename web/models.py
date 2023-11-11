from django.db import models

class Loans(models.Model):
    dni = models.CharField(max_length=8)
    name_and_last_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], default='M')
    email = models.EmailField()
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    



class Users(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=True)