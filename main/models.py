from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    class Meta:
        abstract = True


class Table(BaseModel):
    number = models.PositiveIntegerField(verbose_name='Номер стола', unique=True)

    def __str__(self):
        return f"Номер стола #{self.number}"

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ['number']
