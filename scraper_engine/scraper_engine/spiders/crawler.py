from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response

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
            Rule(LinkExtractor(unique=True), callback='parse'),
        ]
        super(ContactSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object.
        i = {}
        i['url'] = response.css('title::text').extract()
        return i


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    start_urls = [
        'https://www.programiz.com/python-programming/if-elif-else'
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
