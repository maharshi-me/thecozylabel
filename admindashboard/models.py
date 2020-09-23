from django.db import models

# Create your models here.
class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=200)
    message = models.CharField(max_length=200000)
    image = models.FileField(upload_to='contact_forms', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
