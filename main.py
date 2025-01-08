import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_short_link(token, url, version="5.199"):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    url_components = urlparse(url)
    key = url_components.path.lstrip("/")
    if not key:
        return False
    params = {
        "access_token": token,
        "v": version,
        "key": key,
        "interval": "forever"
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    check = response.json()
    if 'error' in check:
        raise ValueError(
            f"{check['error']['error_msg']}\n"
            f"{check['error']['error_code']}"
        )
    return True


def shorten_link(token, url, version="5.199"):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        "access_token": token,
        "v": version,
        "url": url,
        "private": 0
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    link = response.json()
    if 'error' in link:
        raise ValueError(
            f"{link['error']['error_msg']}\n"
            f"Код ошибки: {link['error']['error_code']}"
        )
    return link['response']['short_url']


def count_clicks(token, short_link, version="5.199"):
    url_components = urlparse(short_link)
    key = url_components.path.lstrip("/")
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        "access_token": token,
        "v": version,
        "key": key,
        "interval": "forever"
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    clicks = response.json()
    if clicks['response']['stats'] == []:
        raise ValueError("Статистики еще нет")
    if 'error' in clicks:
        raise ValueError(
            f"{clicks['error']['error_msg']}"
            f"Код ошибки: {clicks['error']['error_code']}"
        )

    return clicks['response']['stats'][0]['views']


def main():
    load_dotenv()
    token = os.environ["VK_TOKEN"]
    url = input("Введите ссылку для сокращения: ")
    try:
        if is_short_link(token, url):
            clicks = count_clicks(token, url)
            print(f'Количество кликов по ссылке: {clicks}')
        else:
            short_link = shorten_link(token, url)
            print(f'Сокращенная ссылка: {short_link}')
    except requests.exceptions.HTTPError as error:
        print(f"HTTP ошибка: {error}")
    except ValueError as error:
        print(f"Ошибка API: {error}")
    except Exception as error:
        print(f"Произошла ошибка: {error}")



if __name__ == "__main__":
    main()
