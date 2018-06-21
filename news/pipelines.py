# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from news.items import NewsItem,SohuItem

class NewsPipeline(object):
    def open_spider(self,spider):

        self.f = open("sina.json","w")
        self.f.write("[")

    def process_item(self, item, spider):
        if isinstance(item,NewsItem):
            item = json.dumps(dict(item),ensure_ascii=False)
            self.f.write(item)
            self.f.write(",\n")
        return item

    def close_spider(self,spider):
        self.f.write("]")
        self.f.close()

class SohuPipeline(object):
    def open_spider(self,spider):
        self.f = open("sohu.json","w")
        self.f.write("[")

    def process_item(self, item, spider):
        if isinstance(item, SohuItem):
            item = json.dumps(dict(item),ensure_ascii=False)
            self.f.write(item)
            self.f.write(",\n")
        return item

    def close_spider(self,spider):
        self.f.write("]")
        self.f.close()