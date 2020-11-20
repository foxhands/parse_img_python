import requests
from bs4 import BeautifulSoup
import urllib.request

headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})
url = "http://www.motorpage.ru/select-auto/by-mark.html"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
#Ищем все изображения
variable = soup.find_all('img')
for tag in variable:
  print(tag.get('alt'))
  img_src = tag.get('src')
  try:
        # Скачиваем файл в папку img
        urllib.request.urlretrieve(img_src, './img/' + tag.get('alt') + '.jpg')
        # Сообщаем что все хорошо
        print('Файл сохранился: ' + img_src, './img/' + tag.get('alt') + '.jpg')
  except:
        # Сообщаем что все плохо
        print('Не получилось сохранить файл')
