from django.db import models
from django.utils import timezone
# Create your models here.

'''
class Users(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<id: {}, username: {}>'.format(self.id, self.username)
'''
class Instance(models.Model):

    user = models.ForeignKey('auth.User')
    instance = models.CharField(max_length=100)
    instance_provider = models.CharField(max_length=100)
    provider_service = models.CharField(max_length=100)

    def __str__(self):
        return '<instance: {}, service: {}>'.format(self.instance, self.instance_provider)


class PingResults(models.Model):

    user = models.ForeignKey('auth.User')
    instance = models.CharField(max_length=100)
    min_ping = models.DecimalField(max_digits=10, decimal_places=4)
    max_ping = models.DecimalField(max_digits=10, decimal_places=4)
    avg_ping = models.DecimalField(max_digits=10, decimal_places=4)
    update_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<instace: {} , min ping: {}, average ping: {}, max ping: {}>'.format(self.instance, self.min_ping, self.avg_ping, self.max_ping)
