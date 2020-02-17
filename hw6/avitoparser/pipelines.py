# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.avito_photo

    def up_props(self, item):
      k = item['prop']
      v = item['propv']
      s = dict()
      for index, i in enumerate(k):
          s[k[index]] = v[index*2+1]
      del (item['prop'])
      del (item['propv'])
      item['prop'] = s
      return (item)

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        i = self.up_props(item)
        collection.insert_one(i)
        return item
