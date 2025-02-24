# containers/models.py

from django.db import models

class Container(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    spec=models.CharField(max_length=250)
    status = models.CharField(max_length=20, choices=[('running', 'Running'), ('stopped', 'Stopped')], default='stopped')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
