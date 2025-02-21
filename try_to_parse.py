import random
import sys
import time

import requests

import logging
import os
from time import process_time


def set_logging_settings() -> None:
    log_dir = 'logs_here'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'logs.log')

    logging.basicConfig(level=logging.INFO, filename=log_file,
                        filemode='w+', encoding='utf-8',
                        format="%(asctime)s %(levelname)s "
                               "%(funcName)s %(message)s")

    logging.info("Были добавлены настройки конфигурации logging.")


def retrieve_response_from_site() -> None:
    response = requests.get(url=get_path(),
                            headers=get_headers_for_request())

    logging.info(f"Получен ответ с сайта. {response.status_code}")
    write_parsed_text_in_file(response)


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

    logging.info("Создан словарь с заголовками для парсинга.")
    return headers


def write_parsed_text_in_file(response: requests.Response) \
        -> None:
    start = process_time()
    src = response.text
    file_encoding: str = response.encoding

    logging.info(f"Кодировка файла: {file_encoding}")

    file_dir = 'txt_here'
    os.makedirs(file_dir, exist_ok=True)
    my_file = os.path.join(file_dir, 'main_html_text.txt')

    try:
        with (open(my_file, mode="w+", encoding=file_encoding)
              as file):
            file.writelines(src)
    except FileNotFoundError:
        logging.warning("Не удалось создать файл.",
                        exc_info=None)
    except Exception as e:
        logging.warning(f"Ошибка: {e}")

    end = process_time()
    logging.info(f"Текст был добавлен в файл по пути" + \
                 f" {my_file}, заняло: {end - start} времени.")


def count_of_vacancies():
    """
    vacancy - взял условно за одну вакансию, нашел одну строку
    совпадение в txt = одна вакансия
    """
    vacancy: list[str] = ['Backend', 'Django', 'Python']
    stop_point: str = "Выберите"

    with (open('txt_here/main_html_text.txt', mode='r',
              encoding='utf-8') as file):
        for line in file:
            one_string_in_file: str = line
            if any(item in one_string_in_file for item in vacancy):
                write_status_indicator()
                logging.info(f'Была найдена вакансия. '
                             f'Записали индикатор \'1\' в file в'
                             f'  dir: tg_bot')

            if stop_point in one_string_in_file:
                break

    logging.info(f'Вакансии еще нет.')


def write_status_indicator() -> None:
    # Записать '1' в status_indicator.txt
    path: str = os.getcwd() + r'\tg_bot\status_indicator.txt'
    try:
        with open(path, mode='w+', encoding='utf-8') as file:
            file.write('1')
            sys.exit()
    except FileNotFoundError:
        logging.warning("Файл не создан.", exc_info=None)
    except Exception as e:
        logging.warning(f"Ошибка: {e}")


def main():
    set_logging_settings()
    while True:
        retrieve_response_from_site()
        count_of_vacancies()
        r = random.randint(1, 61)
        time.sleep(1178 + r)


if __name__ == "__main__":
    main()
