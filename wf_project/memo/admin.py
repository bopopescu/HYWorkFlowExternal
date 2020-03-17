from django.contrib import admin
from .models import Memo, MemoCC

class MemoCCInline(admin.StackedInline):
    model = MemoCC
    extra = 1

class MemoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['company', 'department', 'project', 'subject']}),
        ('Document Information', {'fields': ['revision','document_number','status','submit_date']}),
        ('Detail', {'fields': ['details']}),
        ('Attachments', {'fields': ['attachment','attachment_date']}),
    ]
    inlines = [MemoCCInline]

admin.site.register(Memo, MemoAdmin)