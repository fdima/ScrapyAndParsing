# 1)Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# *название источника,
# *наименование новости,
# *ссылку на новость,
# *дата публикации
# 2)Сложить все новости в БД

from pprint import pprint
from lxml import html
import requests
import datetime

now = datetime.datetime.now()

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def request_to_lenta_ru():
    target = list()
    try:
        response = requests.get('https://lenta.ru/',
                     headers = header
                    )
        root = html.fromstring(response.text)
        items = root.xpath("//div[@class='item news b-tabloid__topic_news']")
        for item in items:
            target_sourse       = 'lenta.ru'
            target_sourse_info  = ''
            target_name         = item.xpath(".//div/h3/a//span/text()")
            target_url          = item.xpath(".//div/h3/a/@href")
            target_date_time    = item.xpath(".//div/span/span[@class='time']/text()")
            target_date         = item.xpath(".//div/span/text()")
            if (target_date[0] == 'Сегодня'):
                target_date = now.strftime("%d %B")
            target.append([target_sourse,target_name,target_url,target_date_time,target_date])
        return (target) 
    except:
        print('Ошибка запроса')

def request_to_yandex_news():
    target = list()
    try:
        response = requests.get('https://yandex.ru/news',
                     headers = header
                    )
        root = html.fromstring(response.text)
        items = root.xpath("//td[@class='stories-set__item']")
        for item in items:
            target_sourse_info  = item.xpath(".//div/div[@class = 'story__info']/div/text()")[0][0:-5].strip()
            target_name         = item.xpath(".//div/div[@class = 'story__topic']/h2/a/text()")
            target_url          = item.xpath(".//div/div[@class = 'story__topic']/h2/a/@href")
            target_date_time    = item.xpath(".//div/div[@class = 'story__info']/div/text()")[0][-5:].strip()
            target_date         = "only news"
            # if (target_date[0] == 'Сегодня'):
                # target_date = now.strftime("%d %B")
            target.append([target_sourse_info,target_name,target_url,target_date_time,target_date])
        return (target) 
    except:
        print('Ошибка запроса')     

def request_detail_to_mail_ru(urls):
    target_sourse_info = list()
    target_date_time = list()
    for url in urls:
        response = requests.get(url,
                     headers = header
                    )
        root = html.fromstring(response.text)
        target_sourse_info.append(root.xpath("//meta[@name='mediator_author']")[0].get('content')) # источник публикации
        target_date_time.append(root.xpath("//meta[@property='article:published_time']")[0].get('content')) # время публикации
    return (target_sourse_info, target_date_time)        # //meta[@name='mediator_author'] //meta[@property='article:published_time']


def request_to_mail_ru():
    target = list()
    try:
        response = requests.get('https://mail.ru/',
                     headers = header
                    )
        # print (response.text)
        root = html.fromstring(response.text)
        # items = root.xpath("//div[contains(@class, 'news-item')]")
        items = root.xpath("//div[@class = 'ssr-main']")
        target_name         = items[0].xpath("./a/text()")
        target_url          = items[0].xpath("./a/@href")
        #     target_date_time    = ''
        target_date         = ''
        target_sourse_info, target_date_time = request_detail_to_mail_ru (target_url)
        target.append([target_sourse_info,target_name,target_url,target_date_time])
        return (target) 
    except:
        print('Ошибка запроса')     



# result = request_to_mail_ru()
# result = request_to_yandex_news()
result = request_to_lenta_ru()

pprint(result)
