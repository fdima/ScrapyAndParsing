# 1)Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# *название источника,
# *наименование новости,
# *ссылку на новость,
# *дата публикации
# 2)Сложить все новости в БД

from pprint import pprint
from lxml import html
# from lxml.etree import tostring
import requests
import datetime
from SQL import Lenta, Yandex, Mailru, openSession, addinSession, closeSession

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
            target_sourse_info  = 'null'
            target_name         = item.xpath(".//div/h3/a//span/text()")[0]
            target_url          = item.xpath(".//div/h3/a/@href")[0]
            target_date_time    = item.xpath(".//div/span/span[@class='time']/text()")[0]
            target_date         = item.xpath(".//div/span/text()")[0]
            if (target_date == 'Сегодня'):
                target_date = now.strftime("%d %B")
            target.append([target_sourse,target_sourse_info,target_name,target_url,target_date_time,target_date])
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
            target_sourse       = 'yandex.ru'
            target_sourse_info  = item.xpath(".//div/div[@class = 'story__info']/div/text()")[0][0:-5].strip()
            target_name         = item.xpath(".//div/div[@class = 'story__topic']/h2/a/text()")[0]
            target_url          = item.xpath(".//div/div[@class = 'story__topic']/h2/a/@href")[0]
            target_date_time    = item.xpath(".//div/div[@class = 'story__info']/div/text()")[0][-5:].strip()
            target_date         = now.strftime("%d %B")
            # if (target_date[0] == 'Сегодня'):
                # target_date = now.strftime("%d %B")
            target.append([target_sourse, target_sourse_info,target_name,target_url,target_date_time,target_date])
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
        target_sourse       = 'mail.ru' 
        target_date         = now.strftime("%d %B")
        target_sourse_info, target_date_time = request_detail_to_mail_ru (target_url)
        for i in range(len(target_sourse_info)):
            # print(f"{target_name[i]}")
            target.append([target_sourse,target_sourse_info[i],target_name[i],target_url[i],target_date_time[i],target_date])
        return (target) 
    except:
        print('Ошибка запроса')     

def save_result(result):
    for r in result:

        if r[0] == 'mail.ru':
            session = openSession()
            addinSession(session, Mailru(r))
            closeSession(session)

        if r[0] == 'lenta.ru':
            session = openSession()
            addinSession(session, Lenta(r))
            closeSession(session)
            # pass

        if r[0] == 'yandex.ru':
            session = openSession()
            addinSession(session, Yandex(r))
            closeSession(session)

        # print (f"{r[0]}; {r[1]}; {r[2].__str__()}; {r[3].__str__()}; {r[4].__str__()}; {r[5]}")
    return (0)

if __name__ == "__main__":

    result = request_to_mail_ru()
    save_result(result)
    result = request_to_yandex_news()
    save_result(result)
    result = request_to_lenta_ru()
    save_result(result)
    # pprint(result)


