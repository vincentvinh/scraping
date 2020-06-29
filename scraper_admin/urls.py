from django.urls import path
from scraper_admin import views as scraper_view

urlpatterns = [
    path('contact/', scraper_view.nouveau_contact, name='contact'),
    path('image/', scraper_view.voir_contacts, name='image'),
]
