from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests

# ищем всегда по всем страницам, которые попадают в выборку 
# s = input ("укажите глубину страницц (число от 1..5):")

main_link = 'https://hh.ru/search/vacancy?'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

L_is_autosearch = 'false'
area = '1'
clusters = 'true'
enable_snippets = 'true'
text = 'Администратор салона красоты'
page = '0'          


params = {'L_is_autosearch':L_is_autosearch,
          'area':area,
          'clusters':clusters,
          'enable_snippets':enable_snippets,
          'text':text,
          'page':page
          }

def loadPage(main_link, params, header):
  response = requests.get(main_link, params=params, headers=header)
  html = bs(response.text,'lxml')
  return html

def findMaxPages(html):
  pmax = 0
  first = html.find('div',{'data-qa':'pager-block'})
  try:
    spans = first.findAll('a', {'class':'HH-Pager-Control'}) 
  except Exception:
    return 0

  for span in spans:
    try:
      if int(span.text) > pmax:
        pmax = int(span.text)
    except Exception:
        pass

  return pmax

def parsePage(html):
  vacansis = html.findAll('div', {'data-qa':'vacancy-serp__vacancy'})
  for vacansi in vacansis:
    site = 'hh.ru'
    name = vacansi.find('a',{'data-qa':'vacancy-serp__vacancy-title'}).text
    url = vacansi.find('a',{'data-qa':'vacancy-serp__vacancy-title'})['href']
    try:
      compensation = vacansi.find('div',{'data-qa':'vacancy-serp__vacancy-compensation'}).text 
    except Exception:
      compensation = 'without paying )'
    print(f"{site};{name};{compensation};{url}")

#  main
html = loadPage(main_link, params, header)
parsePage(html)

PageMax = findMaxPages(html) 

if PageMax > 0:
  for i in range(1, PageMax):
    params['page'] = i
    # print (params)
    parsePage(loadPage(main_link, params, header))    