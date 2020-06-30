import scrapy

from scraper_engine.items import ContactItem


class ContactSpider(scrapy.Spider):
    name = "contactSpider"
    start_urls = ["https://www.theodo.co.uk/team"]

    # this is what start_urls does
    # def start_requests(self):
    #     urls = ['https://www.theodo.co.uk/team',]
    #     for url in urls:
    #       yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = ContactItem()
            if sel.xpath('a/@href').extract()[0]:
                item["nom"] = sel.xpath('a/@href').extract()[0]
            else:
                item["nom"] = 'zerzer'
            if sel.xpath('a/@href').extract()[0]:   
                item["photo"] = sel.xpath('a/@href').extract()[0]
            else:
                item["photo"] = 'zerzer'
            if sel.xpath('a/@href').extract()[0]:
                item["adresse"] = sel.xpath('a/@href').extract()[0]
            else:
                item["adresse"] = 'zerzer'

            yield item


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    start_urls = [
        'https://www.lazada.vn/catalog/?from=input&q=lipstick',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
