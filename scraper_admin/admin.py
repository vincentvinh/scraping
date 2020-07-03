from django.contrib import admin
from django.utils.text import Truncator
from scraper_admin.models import ScrapyOrder, ScrapyItem


class ScrapyOrderAdmin(admin.ModelAdmin):
    # Configuration de la liste d'articles
    list_display = ('unique_id', 'data', 'date')
    list_filter = ('data', 'date',)
    date_hierarchy = 'date'
    ordering = ('date',)


class ScrapyItemAdmin(admin.ModelAdmin):
    # Configuration de la liste d'articles
    list_display = ('alt', 'url')


admin.site.register(ScrapyOrder, ScrapyOrderAdmin)
admin.site.register(ScrapyItem, ScrapyItemAdmin)
