from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.spiders.avito import AvitoSpider
from avitoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoSpider, section='avtomobili')  # 'kvartiry'
    process.start()


#запуск краулера scrapy crawl hhru
# os.system("scrapy crawl yourspider")
# https://vike.io/ru/174496/
# https://docs.scrapy.org/en/latest/intro/tutorial.html
# https://coderlessons.com/tutorials/devops/uchitsia-scrapy/scrapy-kratkoe-rukovodstvo