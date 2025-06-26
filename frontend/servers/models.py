from django.db import models

# Create your models here.
class Server(models.Model):
    address = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.address
    
    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'
