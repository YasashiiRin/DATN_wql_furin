from django.db import models

class User(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField()
    password= models.CharField(max_length=18)
    address =models.CharField(max_length=100, null=True)
    phone =models.IntegerField(null=True)
    class Meta:
        db_table = 'user'