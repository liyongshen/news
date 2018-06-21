# -*- coding: utf-8 -*-
import json

import scrapy
from news.items import NewsItem

class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    i = 1
    base_url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=67&lid=566&num=50&page={}'
    start_urls = [base_url.format(i)]


    def parse(self, response):
        res_list = json.loads(response.body.decode())
        data_list = res_list["result"]["data"]
        if data_list:
            for data in data_list:
                item = NewsItem()
                item["title"]=data["title"]
                item["url"]=data["url"]
                item["keywords"]=data["keywords"]
                item["media_name"]=data["media_name"]
                yield scrapy.Request(item["url"],
                                     callback=self.parse_content,
                                     meta={"item":item})

            self.i += 1
            new_url = self.base_url.format(self.i)
            # 必须添加referer为none，否则返回403
            yield scrapy.Request(new_url,callback=self.parse,headers={"referer": "None"})

    def parse_content(self,response):

        item = response.meta["item"]
        item["time"]=response.xpath('//div[@class = "date-source"]/span[1]/text()').extract_first()
        # 返回列表
        item["content"] = response.xpath('//div[@id = "artibody"]/p').xpath("string(.)").extract()
        yield item