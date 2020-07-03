from pprint import pprint
from pymongo import MongoClient
from datetime import datetime
from lxml import html
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
news = []
def mail():
    response = requests.get('https://news.mail.ru/', headers=header)
    dom = html.fromstring(response.text)
    # links = dom.xpath("//a[contains(@class,'link_cropped_no')]/@href | //a[contains(@class,'organic__url_type_oneline')]/@href")
    blocks = dom.xpath("//div[@class='block']//li | //a[@class='photo photo_full photo_scale js-topnews__item']")


    for block in blocks:
        item = {}
        name = block.xpath(".//a[@class='list__text']/text() | .//span[@class='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/text()")
        a = block.xpath(".//@href")

        if a[0].find('sportmail')>0:
            response = requests.get(a[0], headers=header)
            dom = html.fromstring(response.text)
            date = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/text()")
            source = dom.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/text()")
        else:
            response = requests.get('https://news.mail.ru' + a[0], headers=header)
            dom = html.fromstring(response.text)
            date = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/text()")
            source = dom.xpath("//span[contains(text(),'Hi-Tech Mail.ru')]/text() | //span[@class='link__text'][contains(text(),'Mail.ru')]/text() | //a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/text()")
            a = 'https://news.mail.ru' + a[0]
        item['name'] = name[0].replace('\xa0',' ')
        item['url'] = a
        item['date'] = str(datetime.now().date()) + ' ' + date[0][0:date[0].find(' ')]
        item['source'] = source
        news.append(item)
    return news


# mail()

def lentaru():
    response = requests.get('https://lenta.ru/', headers=header)
    dom = html.fromstring(response.text)
    blocks = dom.xpath("//section[contains(@class, 'js-top-seven')]//time[contains(@class, 'g-time')]")
    # news = []
    for b in blocks:
        item = {}
        name = b.xpath("..//text()")
        a = b.xpath("..//@href")
        date = b.xpath("./@datetime")
        source = 'lenta.ru'
        item['name'] = name[1].replace('\xa0',' ')
        item['url'] = a
        item['date'] = date
        item['source'] = 'https://lenta.ru' + source[0]
        news.append(item)
    return news
    # pprint(news)

def yanews():
    response = requests.get('https://yandex.ru/news/', headers=header)
    dom = html.fromstring(response.text)
    blocks = dom.xpath("//div[contains(@class, 'story_notags')]")
    # news = []
    for b in blocks:
        item = {}
        name = b.xpath(".//text()")
        a = b.xpath("./div[@class='story__topic']//@href")
        date = b.xpath(".//div[@class='story__date']/text()")
        source = b.xpath(".//div[@class='story__date']/text()")
        item['name'] = name[0].replace('\xa0',' ')
        item['url'] = a
        item['date'] = str(datetime.now().date()) + ' ' + date[0][-5:]
        item['source'] = source[0][:source[0].rfind(' ')]
        news.append(item)
        return news
# print(news)

mail()
lentaru()
yanews()
# print(news)
client = MongoClient('localhost',27017)
db = client['news_parsing']

novosti = db.novosti
for n in news:
    novosti.insert_one(n)

client.close()