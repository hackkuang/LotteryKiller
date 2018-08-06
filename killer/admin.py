from django.contrib import admin

from .models import Result


class ResultAdmin(admin.ModelAdmin):
    list_display = ('period', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue')
    ordering = ['period']

# Register your models here.
admin.site.register(Result)
