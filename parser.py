import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def is_english(text):
    """
    Проверяет, содержит ли текст только английские буквы, цифры, пробелы и дефисы.
    """
    return bool(re.match(r'^[a-zA-Z0-9\s\-_]+$', text))


def extract_links_and_images(base_url, save_dir="images", links_file="links.txt"):
    """
    Извлекает ссылки и изображения с сайта. Сохраняет только ссылки с английскими именами в файл.
    """
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()  # Проверка статуса ответа
    except requests.RequestException as e:
        print(f"Failed to fetch {base_url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # создаем папку для сохранения изображений, если ее еще нет
    os.makedirs(save_dir, exist_ok=True)

    links = []

    # обрабатываем все элементы <li> с классом
    items = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 zero-padding")

    for item in items:
        # ищем ссылку <a> внутри <li>
        link_tag = item.find('a')
        img_tag = item.find('img')

        if not link_tag or not img_tag:
            continue

        # получаем ссылку и текст альтернативного имени
        link_url = urljoin(base_url, link_tag.get('href'))
        img_url = urljoin(base_url, img_tag.get('src'))  # преобразуем относительный путь в абсолютный
        img_name = img_tag.get('alt', '').strip()

        # проверяем, содержит ли имя только английские буквы
        if not img_name or not is_english(img_name):
            print(f"Skipping non-English name: {img_name}")
            continue

        # нормализуем имя файла
        img_name = re.sub(r'[^\w\-_]', '_', img_name)

        # добавляем ссылку в список
        links.append(link_url)

        # сохраняем изображение
        download_image(img_url, img_name, save_dir)

    # сохраняем ссылки в файл
    with open(links_file, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(f"{link}\n")

    print(f"Links saved to {links_file}")


def download_image(url, img_name, save_dir="images"):
    """
    Функция загрузки изображения по ссылке и сохранения его с заданным именем.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return

    filename = os.path.join(save_dir, f"{img_name}.jpg")
    try:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image saved: {filename}")
    except IOError as e:
        print(f"Failed to save image {img_name}: {e}")


# URL сайта
url = "http://www.motorpage.ru/select-auto/by-mark.html"
extract_links_and_images(url)
