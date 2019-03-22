from django.contrib import admin

from example.models import Document

class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information',
            {'fields': ['name', 'doc_file']}
        ),
    ]
    list_display = ['id', 'name', 'doc_file']
    search_fields = ['name', 'doc_file']
    list_filter = ['name', 'doc_file']

admin.site.register(Document, DocumentAdmin)
