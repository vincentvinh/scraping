import Rule as Rule
from scrapy.linkextractors import LinkExtractor
import scrapy


class ContactSpider(scrapy.Spider):
    name = "crawler"

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        ContactSpider.rules = [
            Rule(LinkExtractor(unique=True), callback='parse_item'),
        ]
        super(ContactSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object.
        i = {}
        i['url'] = response.url
        return i


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    start_urls = [
        'https://www.lazada.vn/catalog/?from=input&q=lipstick',
        "https://shopee.vn/search?keyword=lipstick&page=0"
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
