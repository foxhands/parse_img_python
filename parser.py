import requests
from bs4 import BeautifulSoup
import urllib.request

headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})
url = "http://www.motorpage.ru/select-auto/by-mark.html"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
variable = soup.find_all('img') #Ищем все изображения
for tag in variable:
  hooks = '' # иногда может понадобится, по умолчанию пустое
  img_src = tag.get('src') # ссылка на картинку
  img_name =  tag.get('alt').replace(' ', '-') # имя картинки
  img_path = './img/' # путь к картинке (не забудь создать папку)
  img_file = '.jpg' # разширение файла
  try:
        urllib.request.urlretrieve( hooks + img_src, img_path + img_name + img_file)         # Скачиваем файл в папку img
        print('Файл сохранился: ' +  img_name + img_file)         # Сообщаем что все хорошо
  except:
        print('Не получилось сохранить файл '+ img_src, img_path + img_name + img_file)        # Сообщаем что все плохо
