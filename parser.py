import os
import requests
from bs4 import BeautifulSoup


def download_images(url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    for i, img_tag in enumerate(img_tags):
        img_url = img_tag.get('src')
        alt_text = img_tag.get('alt', str(i))
        filename = f"{alt_text.replace(' ', '-')}.jpg"
        filepath = os.path.join(output_dir, filename)

        response = requests.get(img_url, headers=headers)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"File saved: {filename}")


if __name__ == '__main__':
    url = 'https://www.motorpage.ru/select-auto/by-mark.html'
    output_dir = './img'
    download_images(url, output_dir)
