# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from scraper_admin.models import ScrapyItem, ScrapyOrder


class ContactPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),  # this will be passed from django view
        )

    def close_spider(self, spider):
        # And here we are saving our crawled data with django models.
        item_order = ScrapyOrder()
        item_order.unique_id = self.unique_id
        item_order.data = json.dumps(self.items)
        item_order.save()

    def process_item(self, item, spider):
        self.items.append(item['url'])

        item_scrapy = ScrapyItem()
        item_scrapy.alt = self.unique_id
        item_scrapy.url = item['url']
        item_scrapy.save()
        return item

