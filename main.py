import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def is_short_link(url):
    parsed = urlparse(url)
    return parsed.netloc == "vk.cc"


def shorten_link(token, url, version="5.199"):
    if not is_valid_url(url):
        raise ValueError('Некорректная ссылка. Проверьте формат URL.')

    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        "access_token": token,
        "v": version,
        "url": url,
        "private": 0
    }

    try:
        responce = requests.get(api_url, params=params)
        responce.raise_for_status()
        data = responce.json()

        if 'error' in data:
            error_msg = data['error'].get('error_msg', 'Неизвестная ошибка')
            raise ValueError(f'Ошибка API: {error_msg}')

        return data['response']['short_url']

    except requests.RequestException as e:
        raise ValueError(f"Ошибка сети: {e}")
    except Exception as e:
        raise ValueError(f"Неизвестная ошибка: {e}")


def count_clicks(token, short_link, version="5.199"):
    parsed = urlparse(short_link)
    key = parsed.path.lstrip("/")
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        "access_token": token,
        "v": version,
        "key": key,
        "interval": "forever"
    }

    try:
        responce = requests.get(api_url, params=params)
        responce.raise_for_status()
        data = responce.json()

        if 'error' in data:
            error_msg = data['error'].get('error_msg', 'Неизвестная ошибка')
            raise ValueError(f'Ошибка API: {error_msg}')

        return data['response']['stats'][0]['views']

    except requests.RequestException as e:
        raise ValueError(f"Ошибка сети: {e}")


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")
    url = input("Введите ссылку для сокращения: ")
    try:
        if is_short_link(url):
            clicks = count_clicks(token, url)
            print(f'Количество кликов по ссылке: {clicks}')
        else:
            short_link = shorten_link(token, url)
            print(f'Сокращенная ссылка: {short_link}')
    except ValueError as e:
        print(f'Ошибка: {e}')


if __name__ == "__main__":
    main()
