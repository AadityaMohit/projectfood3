from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    price = models.IntegerField()
    landmark = models.CharField(max_length=255)


    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.CharField(max_length=30) 
    def __str__(self):
        return self.name
    