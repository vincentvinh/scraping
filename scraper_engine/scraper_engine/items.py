from scraper_admin.models import Contact
from scrapy_djangoitem import DjangoItem


class ContactItem(DjangoItem):
    # define the fields for your item here like:
    django_model = Contact
