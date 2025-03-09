from django.contrib import admin

from main.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass
