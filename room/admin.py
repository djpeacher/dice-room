from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'room', 'created')


admin.site.register(Message, MessageAdmin)
