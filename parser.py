import os
import requests
from bs4 import BeautifulSoup


def download_image(url, img_name):
    """
    Функция загрузки изображения по ссылке и сохранения его с заданным именем.
    """
    response = requests.get(url)
    filename = os.path.join("images", f"{img_name}.jpg")
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Image saved: {filename}")


url = "http://www.motorpage.ru/select-auto/by-mark.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# создаем папку для сохранения изображений, если ее еще нет
os.makedirs("images", exist_ok=True)

# получаем все теги img
img_tags = soup.find_all('img')

for img_tag in img_tags:
    # получаем ссылку на изображение и имя марки автомобиля
    img_url = img_tag.get('src')
    img_name = img_tag.get('alt')

    # пропускаем изображения, у которых нет альтернативного текста или ссылки на изображение
    if not img_name or not img_url:
        continue

    # получаем расширение файла
    ext = os.path.splitext(img_url)[1]

    # загружаем изображение только если расширение соответствует изображению
    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
        continue

    download_image(img_url, img_name)
