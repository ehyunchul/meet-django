"""Django Admin
"""
from django.contrib import admin
from hello.models import Messages


class MessagesAdmin(admin.ModelAdmin):
    """MessagesAdmin
    """
    list_display = ('message', 'created', 'updated',)
    search_fields = ('message', 'created',)
    ordering = ('created',)


admin.site.register(Messages, MessagesAdmin)
