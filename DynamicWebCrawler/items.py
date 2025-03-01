# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DynamicwebcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls = scrapy.Field()
    publish_date = scrapy.Field()
    title = scrapy.Field()
    tab_title = scrapy.Field()
    file_name = scrapy.Field()
    pass
