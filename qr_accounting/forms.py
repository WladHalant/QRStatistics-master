from django.forms import ModelForm, TextInput
from django import forms
from qr_accounting.models import Lecture, Listener
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


# Класс формы, который относятся для создания или редактирования заявок
# def get_my_choices():
#     return [(g.name, g.name) for g in Group.objects.filter(~Q(name='executor'))]


class LectureForm(ModelForm):
    group = forms.ModelChoiceField(label='Группа', queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))

    user = None
    usergroups = None

    def __init__(self, *args, **kwargs):
        self.usergroups = Group.objects.filter(~Q(name='executor'))
        super(LectureForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = self.usergroups

    # def __init__(self, *args, **kwargs):
    #     self.group = Group.objects.filter()
    #     super(LectureForm, self).__init__(*args, **kwargs)
    #     self.fields['group'].choices = get_my_choices()

    class Meta:
        # Присваивание сущности заявки
        model = Lecture
        # Поля сущности
        fields = ['topic', 'description', 'group', 'status']

        # Настройка отображения
        labels = {
            # 'date': _('Дата (yyyy-mm-dd HH:MM):'),
            'topic': _('Тема:'),
            'description': _('Описание:'),
            # 'check': _('Статус'),
            'group': _('Группа'),
            'status': _('Статус'),
        }


        # Применение css классов к полям формы
        widgets = {
            'date': TextInput(attrs={'class': 'form-control'}),
            'topic': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


# Класс формы для слушателя
class ListenerForm(ModelForm):
    class Meta:
        model = Listener
        fields = ['phone']
        labels = {
            'phone': _('Введите свой номер телефона, чтобы отметится на лекции (без кода страны): '),
        }
        widgets = {
            'phone': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'XXXXXXXXXX'}),
        }

    # проверка корректности ввода телефона слушателем
    def clean_phone(self):
        # Присваивание результата ввода слушателя
        new_phone = self.cleaned_data['phone']
        # Проверка если не цифры
        if not new_phone.isdigit():
            raise ValidationError('Номер телефона должен состоять только из цифр')
        # Проверка если кол-во цифр не равно 10
        if len(new_phone) != 10:
            raise ValidationError("не соответствует формату (XXXXXXXXXX, без кода страны)")
        return new_phone
