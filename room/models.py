from django.db import models


class Message(models.Model):
    room = models.CharField(max_length=128)
    user = models.CharField(max_length=128)
    message = models.TextField()
