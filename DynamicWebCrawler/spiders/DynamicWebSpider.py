import os
import platform

import scrapy
from scrapy.utils.project import get_project_settings

from DynamicWebCrawler.items import DynamicwebcrawlerItem
from DynamicWebCrawler.utils.DynaUtils import Utils
from scrapy import signals


class DynamicwebspiderSpider(scrapy.Spider):
    name = "DynamicWebSpider"
    allowed_domains = ["jiangsu.gov.cn"]

    def start_requests(self):
        urls = [
            # ('事业', 'http://jshrss.jiangsu.gov.cn/col/col57210/index.html'),
            # ('企业', 'http://jshrss.jiangsu.gov.cn/col/col57211/index.html'),
            ('民办非企业社团', 'http://jshrss.jiangsu.gov.cn/col/col57212/index.html')
        ]
        for tab_title, url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'tab_title': tab_title})

    def parse(self, response):
        tab_title = response.meta['tab_title']
        records = response.xpath("//div[contains(@class,'default_pgContainer')]/li")
        for record in records:
            title = record.xpath("./a/@title").extract_first()
            url = record.xpath("./a/@href").extract_first()
            url = response.urljoin(url)

            publish_date = record.xpath("./a/span[2]/text()").extract_first()
            yield scrapy.Request(url=url, callback=self.parse_content,
                                 meta={'title': title,
                                       'url': url,
                                       'publish_date': publish_date,
                                       'tab_title': tab_title})
        next_page = response.xpath("//a[contains(@class,'default_pgNext')]/@href").extract_first()
        next_page_disabled = response.xpath("//a[contains(@class,'default_pgNextDisabled')]/@href").extract_first()

        if next_page and next_page_disabled is None:
            next_page = response.urljoin(next_page)
            print('--->', tab_title, next_page, '<---')
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'tab_title': tab_title})

    def parse_content(self, response):
        title = response.meta['title']
        # url = response.meta['url']
        publish_date = response.meta['publish_date']
        tab_title = response.meta['tab_title']
        docs = response.xpath("//div[contains(@class,'wsbs-center-nr0-nr')]//a")
        if len(docs) > 0:
            for doc in docs:
                file_urls = list()
                file_name = doc.xpath("./text()").extract_first()
                file_url = doc.xpath("./@href").extract_first()
                if file_name is None or file_name == '' or 'mailto' in file_url:
                    continue

                file_url = response.urljoin(file_url)
                file_urls.append(file_url)
                item = DynamicwebcrawlerItem()
                item["title"] = title
                item["file_name"] = file_name
                item["publish_date"] = publish_date
                item["tab_title"] = tab_title
                item["file_urls"] = file_urls
                print(tab_title, '/', title, '/', file_name)
                yield item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self, spider):
        self.driver = Utils.init_broswer_driver()

    def spider_closed(self, spider):
        self.driver.close()
        Utils.close_chrome()
