from django.db import models


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=128)
    user = models.CharField(max_length=128)
    message = models.TextField()

    def __str__(self):
        return self.message
