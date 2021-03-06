# Generated by Django 3.0.2 on 2021-03-20 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField()),
                ('topic', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('uuid', models.CharField(blank=True, max_length=200, unique=True)),
                ('check', models.BooleanField(default=True)),
                ('group', models.CharField(choices=[('group1', 'Группа поддержки пользователей'), ('group2', 'Группа сетевых технологий'), ('group3', 'Группа разработки')], default='group1', max_length=6)),
                ('lecturer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listener',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(max_length=10, null=True)),
                ('lecture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='qr_accounting.Lecture')),
            ],
        ),
    ]
