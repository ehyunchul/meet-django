from django.db import models

# Create your models here.


class Hello(models.Model):
    """만나면 반가워서 Hello"""
    message = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message
