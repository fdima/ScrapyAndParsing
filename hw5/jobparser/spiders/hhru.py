# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import HHItem
# from items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'

    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=%D0%90%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%BE%D1%80&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').extract():
            yield response.follow(link, callback=self.parse_vacancy)

    @staticmethod
    def parse_vacancy(response: HtmlResponse):
        item = {
          'title': response.xpath('//h1[@class="header"]//text()').extract_first(),
          'company': response.xpath('//a[@class="vacancy-company-name"]//text()').extract(),
          'min_salary': response.xpath('//meta[@itemprop="minValue"]/@content').extract_first(),
          'max_salary': response.xpath('//meta[@itemprop="maxValue"]/@content').extract_first(),
          'salary':  response.xpath('//script[@type="application/ld+json"]//text()').extract_first(), 
          'currency': response.xpath('//meta[@itemprop="currency"]/@content').extract_first(),
          'unit': response.xpath('//meta[@itemprop="unitText"]/@content').extract_first(),
          'location': response.xpath('//span[@data-qa="vacancy-view-raw-address"]//text()').extract(),
          'alt_location': response.xpath('//span[@itemprop="jobLocation"]/..//text()').extract(),
          'link': response.url
        }

        yield HHItem(**item)

# //script[@type='application/ld+json']