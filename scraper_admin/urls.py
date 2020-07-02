from django.urls import path
from scraper_admin import views as scraper_view

urlpatterns = [
    path('contact/', scraper_view.nouveau_contact, name='contact'),
    path('launch/', scraper_view.launch_spider, name='launch_spider'),
    path('', scraper_view.chart, name='chart'),
]
