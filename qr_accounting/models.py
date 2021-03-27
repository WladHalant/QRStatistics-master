from django.contrib.auth.models import User, Group
from django.utils.functional import lazy
from django.db import models
from django.db.models import Q
# from qr_accounting.service import get_group


class Lecture(models.Model):
    # Автоматическая запись даты для сортировки card
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата в заявке
    # date = models.DateTimeField()
    # Тема заявки
    topic = models.CharField(max_length=200)
    # Описание заявки (не обязательное поле)
    description = models.CharField(max_length=500, blank=True)
    # Лектор(Связь )
    lecturer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Уникальное значение для добавления к ссылке на регистрацию заявки
    uuid = models.CharField(max_length=200, blank=True, unique=True)
    # Статус
    # check = models.BooleanField(default=True)

    # GROUP_CHOICES = [(g.name, g.name) for g in Group.objects.filter(~Q(name='executor'))]
    # group = models.CharField(max_length=100, choices=GROUP_CHOICES, default=GROUP_CHOICES[0])


    group = models.CharField(max_length=100)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)

    STATUS_CHOICES = (
        ('Выполнена', 'Выполнена'),
        ('В работе', 'В работе'),
        ('Отменена', 'Отменена')
    )

    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[1])

    def __str__(self):
        return f"{self.topic}"


# Сущность слушателя
class Listener(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # заявка
    lecture = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True)
    # Номер телефона
    phone = models.CharField(max_length=10, null=True)
