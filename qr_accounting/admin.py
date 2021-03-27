from django.contrib import admin

from qr_accounting.models import Lecture


@admin.register(Lecture)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("topic", "group", "created_at", "status")
    list_filter = ("status", "group")
