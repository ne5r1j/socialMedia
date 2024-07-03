from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    #on_delete --> if model is deleted profile of user should be deleted
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)#linking with the USERS model
    photo = models.ImageField(upload_to='users/%Y/%M/%d', blank=True) 

    def __str__(self):
        return self.user.username
    