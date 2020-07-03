from django.contrib import admin
from django.utils.text import Truncator
from scraper_admin.models import ScrapyOrder, ScrapyItem


class ScrapyItemAdmin(admin.ModelAdmin):
    # Configuration de la liste d'articles
    list_display = ('unique_id', 'data', 'date')
    list_filter = ('data', 'date',)
    date_hierarchy = 'date'
    ordering = ('date',)


admin.site.register(ScrapyOrder, ScrapyItemAdmin)
admin.site.register(ScrapyItem)
