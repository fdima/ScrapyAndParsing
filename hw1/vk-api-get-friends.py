from pprint import pprint
import requests
import json
#e5e4cd692a72b0b66ea0a6b80255d1c3
#https://api.vk.com/method/friends.get?v=5.103&access_token=07a38b9007a38b9007a38b900607cce39a007a307a38b9059913d3beb12c6d89837fbbc&user_id=26949941

main_link = 'https://api.vk.com/method/friends.get'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

v = '5.103'
access_token = '07a38b9007a38b9007a38b900607cce39a007a307a38b9059913d3beb12c6d89837fbbc'
user_id = '26949941'

params = {'access_token':access_token,
          'user_id':user_id,
          'v':v,
          }

response = requests.get(main_link,params=params)
if response.ok:
    data = json.loads(response.text)
    pprint(data['response']['items'])
    #print(f"В городе {data['name']} температура {data['main']['temp'] - 273.15} градусов")
