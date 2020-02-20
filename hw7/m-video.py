from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from hashlib import sha1
import time

class DB:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.mvideo

    def get_attr(self, item, css_class):
        try:
            text = item.find_element_by_class_name(css_class).text
            if not text or text == '':
                return None
        except:
            return None
        return int(''.join(filter(lambda x: x.isdigit(), text)))


    def insert_data(self, carousel):
        goods = carousel.find_elements_by_class_name('gallery-list-item')
        for good in goods:
            title = good.find_element_by_class_name('sel-product-tile-title').text
            if title:
                item = {
                    '_id': sha1(title.encode('utf-8')).hexdigest(),
                    'title': title,
                    'price': self.get_attr(good, 'c-pdp-price__current'),  # Текущая цена
                    'discount': self.get_attr(good, 'c-pdp-price__discount'),
                    'trade-price': self.get_attr(good, 'c-pdp-price__trade-price'),
                    'monthly': self.get_attr(good, 'c-pdp-price__monthly')
                }

                self.db['hits'].update_one({'_id': item['_id']},
                                           {'$set': item},
                                           upsert=True)
                print('insert good ...')


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.mvideo.ru/')

    carousel = driver.find_element_by_xpath('//div[contains(text(), "Хиты продаж")]/../../..')
    ActionChains(driver).move_to_element(carousel).perform()
    # print('переместили курсор к карусели')

    next_btn = carousel.find_element_by_xpath('//div[contains(text(), "Хиты продаж")]/../../..//a[contains(@class, "next-btn")]')

    db = DB()
    db.insert_data(carousel)
    while next_btn.is_displayed():
        next_btn.click()
        print('next page ...')
        time.sleep(2)  # Ждем завершения анимации
        db.insert_data(carousel)

    driver.quit()