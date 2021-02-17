from __future__ import absolute_import

from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import Rule
import re
from ..utils.spiders import BasePortiaSpider

import pymongo
from pymongo import MongoClient

import sys

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.haber
haber = db.hurriyetnews
linklerd = db.linkler



class duyguyeni(BasePortiaSpider):
    name = "hurriyet_news"
    allowed_domains = ['hurriyetdailynews.com']
    start_urls = ['https://www.hurriyetdailynews.com/']
    rules = [
        Rule(
            LinkExtractor(

                #deny=['/secim']


            ),
            callback='parse_item',
            follow=True
        )
    ]

    def parse_item(self, response):
        try:
            try:
                url = str(response.request.url).split("-")
                haber_id = str(url[len(url)-1]).split('.')[0]
                title = response.xpath('/html/body/div[2]/div[4]/div[1]/div[2]/h1/text()').get()
                img = response.xpath('/html/body/div[2]/div[4]/div[1]/div[2]/img/@data-src').get()
                tarih = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/ul[2]/li/text()').get()
                kategori = response.xpath('/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/ul[1]/li[2]/a/text()').get()
                # print("tarih" + str(tarih))
                news_1 = response.xpath('/html/body/div[2]/div[4]/div[1]/div[2]/p/text()').get()
                news_all = ""
                news_all = news_all + " " + news_1

                for i in range(20):
                    try:
                        news = response.xpath('/html/body/div[2]/div[4]/div[1]/div[2]/p[' + str(i) + ']/text()').get()
                        if news is not None:
                            news_all = news_all + str(news)
                    except:
                        print("haber sonu-----------------")
                # print(str(news_all))
                if tarih is None or title  is None or news_all is None:
                    print("boş verisi olan haber")
                else:
                    new_haber = {'url': str(response.request.url), "haber_id": str(tarih) + str(title),
                                 "title": str(title),"tarih":tarih,"kategori":kategori,
                                 "img": str(img), 'haber': str(news_all)}
                    x = haber.insert_one(new_haber)
            except:
                print("Hata normal-haber")

        except:
            print('hata bilinmeyen')
        new_link = {'url': str(response.request.url)}
        x = linklerd.insert_one(new_link)