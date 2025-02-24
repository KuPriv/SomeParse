import random
import sys
import time
import os
import logging

import requests
from requests import Response
from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString


def set_logging_settings() -> None:
    log_dir = 'logs_here'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'logs.log')

    logging.basicConfig(level=logging.INFO, filename=log_file,
                        filemode='w+', encoding='utf-8',
                        format="%(asctime)s %(levelname)s "
                               "%(funcName)s %(message)s")

    logging.info("Были добавлены настройки конфигурации logging.")


def check_vacancies() -> None:
    vacancy: list[str] = ['Backend', 'Django', 'Python']
    response = retrieve_response_from_site()
    line = get_html_with_vacancies(response)

    for item in line:
        if any(keyw in item.text for keyw in vacancy):
            logging.info(f'Была найдена вакансия: {item.text}')
            write_status_indicator(item.text)


    logging.info(f'Вакансии еще нет.')


def retrieve_response_from_site() -> Response:
    response = requests.get(url=get_path(),
                            headers=get_headers_for_request())
    logging.info(f"Получен ответ с сайта. {response.status_code}")
    return response


def get_path() -> str:
    return "https://rabota.medrocket.ru/student"


def get_headers_for_request() -> dict[str, str]:
    st_user_agent: str = ("Mozilla/5.0 (Windows NT 10.0; " +
                          "Win64; x64) AppleWebKit/537.36 " +
                          "(KHTML, like Gecko) ") + \
                         "Chrome/132.0.0.0 Safari/537.36"
    st_accept: str = "text/html"

    headers: dict[str, str] = {
        "User-Agent": st_user_agent,
        "Accept": st_accept,
    }

    logging.info("Создана хэш-таблица с заголовками для парсинга.")
    return headers


def get_html_with_vacancies(response: requests.Response) -> ResultSet[PageElement | Tag | NavigableString]:
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all("div", class_="t1025__title t-name t-name_md js-product-name")


def write_status_indicator(s: str) -> None:
    try:
        with open(path_for_status_indicator(), mode='w+', encoding='utf-8') as file:
            file.write(f'{s[1:-1]}')
            logging.info(f'Записали вакансию в file в dir: tg_bot')
            sys.exit()
    except Exception as e:
        logging.warning(f"Ошибка: {e}")


def clean_status_indicator() -> None:
    with open(path_for_status_indicator(), mode='w', encoding='utf-8'):
        pass


def path_for_status_indicator() -> str:
    return os.getcwd() + r'\tg_bot\status_indicator.txt'


def main():
    set_logging_settings()
    clean_status_indicator()
    while True:
        check_vacancies()
        r = random.randint(1, 61)
        time.sleep(900 + r)


if __name__ == "__main__":
    main()
