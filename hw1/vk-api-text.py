from pprint import pprint
import requests
import json
#e5e4cd692a72b0b66ea0a6b80255d1c3


main_link = 'https://oauth.vk.com/authorize'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
client_id = '7301130'
redirect_uri = 'https://oauth.vk.com/blank.htm'
response_type = 'token'
scope = '2'
v = '5.52'
state = ''
display = 'page'
m = '4'
email = ''


params = {'client_id':client_id,
          'redirect_uri':redirect_uri,
          'response_type':response_type,
          'scope':scope,
          'v':v,
          'state':state,
          'display':display,
          'm':m,
          'email':email
          }

response = requests.get(main_link,params=params)
print (response.text)
if response.ok:
    data = json.loads(response.text)
    pprint(data)
    #print(f"В городе {data['name']} температура {data['main']['temp'] - 273.15} градусов")
