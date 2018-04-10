"""Django Admin
"""
from django.contrib import admin
from hello.models import Hello

class HelloAdmin(admin.ModelAdmin):
    """HelloAdmin
    """
    list_display = ('message', 'created', 'updated',)
    search_fields = ('message', 'created',)
    ordering = ('created',)

admin.site.register(Hello, HelloAdmin)
