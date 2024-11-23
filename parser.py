import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_image(url, img_name, save_dir="images"):
    """
    Загружает изображение по ссылке и сохраняет его с заданным именем.
    
    :param url: Ссылка на изображение.
    :param img_name: Имя файла для сохранения.
    :param save_dir: Каталог для сохранения изображений.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return
    
    os.makedirs(save_dir, exist_ok=True)  # Создаем папку, если она не существует
    filename = os.path.join(save_dir, f"{img_name}.jpg")
    
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Image saved: {filename}")


def get_absolute_url(base_url, relative_url):
    """
    Преобразует относительный путь в абсолютный.
    
    :param base_url: Базовый URL.
    :param relative_url: Относительный путь.
    :return: Абсолютный URL.
    """
    return urljoin(base_url, relative_url)


def parse_and_download_images(base_url, save_dir="images"):
    """
    Парсит изображения на странице и скачивает их.
    
    :param base_url: Ссылка на страницу для парсинга.
    :param save_dir: Каталог для сохранения изображений.
    """
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        img_name = img_tag.get('alt')

        # Пропуск изображений без alt или src
        if not img_name or not img_url:
            continue

        # Преобразуем относительный путь в абсолютный
        img_url = get_absolute_url(base_url, img_url)

        # Проверяем допустимое расширение
        ext = os.path.splitext(img_url)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            continue

        download_image(img_url, img_name, save_dir)


if __name__ == "__main__":
    BASE_URL = "http://www.motorpage.ru/select-auto/by-mark.html"
    SAVE_DIR = "images"

    parse_and_download_images(BASE_URL, SAVE_DIR)
