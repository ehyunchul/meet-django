# coding=utf-8

"""Hello models
"""
from django.db import models
from django.utils import timezone

class Hello(models.Model):
    """만나면 반가워서 Hello
    """

    message = models.CharField('인사말', max_length=250)
    created = models.DateTimeField('생성일', auto_now_add=True)
    updated = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = '헬로'
        verbose_name_plural = '헬로~'
