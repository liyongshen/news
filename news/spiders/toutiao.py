# -*- coding: utf-8 -*-

# 根据分析，不使用scrapy，只用selenium

import json

import requests
import time
from selenium import webdriver
import re
from selenium.webdriver.chrome.options import Options


class toutiao_spider(object):
    def __init__(self):
        # 有界面
        # self.driver = webdriver.Chrome()
        # 无界面
        self.op = Options()
        self.op.set_headless()
        self.driver = webdriver.Chrome(options=self.op)
        self.driver.get('https://www.toutiao.com/ch/news_regimen/')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'referer': 'https://www.toutiao.com/ch/news_regimen/'
            }
        self.f = open("toutiao.json", "w", encoding="utf8")

    def get_data(self, i):

        data_list = []
        # 判断是否到尾了
        try:
            # 利用position和i爬取新增li
            li_s = self.driver.find_elements_by_xpath(
                '//div[@class = "wcommonFeed"]/ul/li[position()>%s and @ga_event = "article_item_click"]' % i)
        except:
            return None
        print(li_s)
        for li in li_s:
            item = {}
            item["authorName"] = li.find_element_by_xpath('.//a[@ga_event = "article_name_click"]').text
            item["url"] = li.find_element_by_xpath('.//a[@class = "link title"]').get_attribute('href')
            item["title"] = li.find_element_by_xpath('.//a[@class = "link title"]').text
            item["comment_num"] = li.find_element_by_xpath('.//a[@class = "lbtn comment"]').text
            # 部分新闻没有图片
            try:
                item["pic_url"] = li.find_element_by_xpath('.//a[@class = "img-wrap"]/img').get_attribute('src')
            except:
                item["pic_url"] = None
            # 利用requests请求新闻详情页
            item = self.get_content(item)
            data_list.append(item)
        return data_list

    def get_content(self, item):
        response = requests.get(item["url"], headers=self.headers)

        html = response.text
        item["time"] = re.findall("time.*?'(.*?)'", html, re.S)
        item["content"] = re.findall("articleInfo.*?content.*?'(.*?)'", html, re.S)
        return item

    def save_data(self, data_list):
        for data in data_list:
            data = json.dumps(data, ensure_ascii=False)
            self.f.write(data)
            self.f.write(",\n")

    def run(self):
        i = 0
        n = 1
        while True:
            data_list = self.get_data(i)
            if not data_list:
                break
            self.save_data(data_list)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            # js = "var q=document.documentElement.scrollTop=2500"
            # self.driver.execute_script(js)
            time.sleep(1)
            if n == 1:
                # 首页默认11个li
                i += 11
                n += 1
                # 第一次需要往上拉一下促发请求
                js = "var q=document.documentElement.scrollTop=0"
                self.driver.execute_script(js)
            else:
                # 每次下拉新增10个li
                i += 10


if __name__ == '__main__':
    toutiao = toutiao_spider()
    toutiao.run()
