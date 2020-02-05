from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests

# ищем всегда по всем страницам, которые попадают в выборку 
# s = input ("укажите глубину страницц (число от 1..5):")
#  транслит https://gist.github.com/ledovsky/6398962
# https://www.superjob.ru/vakansii/administrator-salona-krasoty.html?geo%5Bt%5D%5B0%5D=4&page=1

main_link0 = 'https://www.superjob.ru/'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

text = 'Администратор салона красоты'
page = '1'          
geo = '4' #Москва

params = {
          'page':page,
          'geo':geo,
          'page':page
          }

def loadPage(main_link, params, header):
  response = requests.get(main_link, params=params, headers=header)
  html = bs(response.text,'lxml')
  return html

def findMaxPages(html):
  pmax = 0
  first = html.find('div',{'class':'L1p51'})
  try:
    spans = first.findAll('span', {'class':'_3IDf-'})
  except Exception:
    return 0

  for span in spans:
    try:
      if int(span.text) > pmax:
        pmax = int(span.text)
    except Exception:
        pass
  return pmax

def ShSumm(s):
  s = s.replace(' ','')
  s = s.replace('\xa0','')
  s = s.replace('\t','')
  s = s.replace('.','')
  s = s.replace('руб','')
  s = s.replace('₽','')
  # s = s.replace('По—говорённости','0—0')
  
  
  if (s[0:2] == 'от'): s = s + '—0'

  s = s.replace('от','')
  s = s.replace('до','—')
  
  if (s[0] == '—'): s = '0' + s

  try:
    s1, s2 = s.split('—')
  except Exception:
    # pass
    s1 = '0'
    s2 = '0'
    # s1 = '$'
    # s2 = '$'

  if (s1 == 'По'): 
    s1 = '0'
    s2 = '0'

  return ([int(s1),int(s2)])
  # print (s,s1,s2, end =" #")
  # return ([0,0])

def parsePage(html):
  vacansis = html.findAll('div', {'class':'f-test-vacancy-item'})
  for vacansi in vacansis:
    site = 'superjob.ru'
    link = vacansi.findAll('a')
    name = link[0].text
    url = main_link0[:-1]+link[0]['href']
    compensation = vacansi.find('span',{'class':'f-test-text-company-item-salary'}).text
    try:
      company = link[1].text 
      companyUrl = main_link0[:-1]+link[1]['href']
    except Exception:
      company = 'none'
      companyUrl = 'none'
    # print(f"{site};{name};{compensation};{url};{company};{companyUrl}")
    sm1, sm2 = ShSumm(compensation)
    print(f"{site};{name};{sm1};{sm2};{url};{company};{companyUrl}")
  return 0

def latinizator(letter):
  legend = {
  'а':'a',
  'б':'b',
  'в':'v',
  'г':'g',
  'д':'d',
  'е':'e',
  'ё':'yo',
  'ж':'zh',
  'з':'z',
  'и':'i',
  'й':'y',
  'к':'k',
  'л':'l',
  'м':'m',
  'н':'n',
  'о':'o',
  'п':'p',
  'р':'r',
  'с':'s',
  'т':'t',
  'у':'u',
  'ф':'f',
  'х':'h',
  'ц':'ts',
  'ч':'ch',
  'ш':'sh',
  'щ':'shch',
  'ъ':'y',
  'ы':'y',
  'ь':"'",
  'э':'e',
  'ю':'yu',
  'я':'ya',
   
  'А':'A',
  'Б':'B',
  'В':'V',
  'Г':'G',
  'Д':'D',
  'Е':'E',
  'Ё':'Yo',
  'Ж':'Zh',
  'З':'Z',
  'И':'I',
  'Й':'Y',
  'К':'K',
  'Л':'L',
  'М':'M',
  'Н':'N',
  'О':'O',
  'П':'P',
  'Р':'R',
  'С':'S',
  'Т':'T',
  'У':'U',
  'Ф':'F',
  'Х':'H',
  'Ц':'Ts',
  'Ч':'Ch',
  'Ш':'Sh',
  'Щ':'Shch',
  'Ъ':'Y',
  'Ы':'Y',
  'Ь':"'",
  'Э':'E',
  'Ю':'Yu',
  'Я':'Ya',

  ' ':'-'
  }

  for i, j in legend.items():
    letter = letter.replace(i, j)
  return letter
 
def makeUrl():
  url = main_link0 +'vakansii/'+ latinizator(str.lower(text)) + '.html?'
  return (url)

#  main

main_link = makeUrl()

html = loadPage(main_link, params, header)

PageMax = findMaxPages(html) 

if PageMax > 0:
  for i in range(1, PageMax+1):
    params['page'] = i
    parsePage(loadPage(main_link, params, header))    
