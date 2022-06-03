from django.contrib import admin
from .models import Note


@admin.register(Note)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('nt_title', 'nt_importance', 'nt_public', 'nt_status', 'nt_endtime', 'id')
    fields = (('nt_title', 'nt_public', 'nt_importance'), 'nt_status', 'nt_description', 'nt_createtime', 'nt_updatetime', 'nt_endtime', 'nt_author')
    readonly_fields = ('nt_createtime', 'nt_updatetime')
    search_fields = ['nt_title', 'nt_description']
    list_filter = ['nt_public', 'nt_importance']
