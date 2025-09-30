# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookscraperItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    about_product = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()

class GutenbergItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    about_book = scrapy.Field()
    kindle_book = scrapy.Field()
