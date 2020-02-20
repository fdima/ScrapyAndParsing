# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import pprint
from scrapy.loader.processors import MapCompose, TakeFirst, Identity


def cleaner_photo(value):
    if value[:2] == '//':
        return f'http://{value}'
    return value

class AvitoparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))  # // -> http://
    propv = scrapy.Field()
    prop = scrapy.Field()
    propa = scrapy.Field()