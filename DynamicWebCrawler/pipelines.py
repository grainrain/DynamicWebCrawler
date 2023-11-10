# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline

from DynamicWebCrawler.settings import FILES_STORE
class DownloadFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        title = item['title']
        tab_title = item['tab_title']
        publish_date = item['publish_date']
        file_name = item['file_name']
        file_urls = item['file_urls']
        file_download_path = f"{tab_title}/{title}/{publish_date}_{file_name}"
        return file_download_path

class CsvPipeline(object):
    def __init__(self):
        store_file = FILES_STORE + '/FilesCrawler.csv'
        self.file = open(store_file, 'a+', encoding="utf-8",newline = '')
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        self.writer.writerow([item['title'], item['hits'], item['publish_date'],item['video_url'], item['image_urls']])
        return item

    def close_spider(self, spider):
        self.file.close()

class DynamicwebcrawlerPipeline:
    def process_item(self, item, spider):
        return item
