# coding=utf-8

"""Hello models
"""
from django.db import models
from django.utils import timezone


class Messages(models.Model):
    """만나면 반가워서 하는말
    """

    message = models.CharField('인사말', max_length=250)
    created = models.DateTimeField('생성일', auto_now_add=True)
    updated = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        # db_table = '사용자 정의 테이블명'
        verbose_name = '인사말'
        verbose_name_plural = '인사말들'
