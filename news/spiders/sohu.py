# -*- coding: utf-8 -*-
import json

import scrapy
from news.items import SohuItem


class SinaSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    i = 1
    base_url = 'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=32&page={}&size=100'
    start_urls = [base_url.format(i)]

    def parse(self, response):
        data_list = json.loads(response.body.decode())
        # 因为很多新闻的链接都是其他网站的，html格式不一致，所有在这里就不爬取各个新闻的内容了
        if data_list:
            for data in data_list:
                item = SohuItem()
                item["authorName"] = data["authorName"]
                item["originalSource"] = data["originalSource"]
                item["title"] = data["title"]
                item["id"] = data["id"]
                item["picUrl"] = data["picUrl"]
                yield item
            self.i += 1
            new_url = self.base_url.format(self.i)

            yield scrapy.Request(new_url, callback=self.parse)

