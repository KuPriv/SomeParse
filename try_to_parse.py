import random
import sys
import time

import requests

import logging
import os
from time import process_time


def set_logging_settings():
    log_dir = 'logs_here'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'logs.log')

    logging.basicConfig(level=logging.INFO, filename=log_file, filemode='w+', encoding='utf-8',
                        format="%(asctime)s %(levelname)s %(funcName)s %(message)s")

    logging.info("Были добавлены настройки конфигурации logging.")


def retrieve_request_text() -> str:
    req = requests.get("https://rabota.medrocket.ru/student", get_headers_for_request())
    src = req.text


    file_encoding: str = req.encoding
    logging.info(f"Кодировка файла: {file_encoding}")

    logging.info("Получен html-text с сайта, передаем в write_parsed_text_in_file()")

    write_parsed_text_in_file(src, file_encoding)
    return src


def get_headers_for_request() -> dict[str, str]:
    st_user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/132.0.0.0 Safari/537.36"
    st_accept: str = "text/html"

    headers: dict[str, str] = {
        "User-Agent": st_user_agent,
        "Accept": st_accept,
    }

    logging.info("Создана хэш-таблица с заголовками для парсинга.")
    return headers


def write_parsed_text_in_file(src: str, file_encoding: str) -> None:
    start = process_time()

    file_dir = 'txt_here'
    os.makedirs(file_dir, exist_ok=True)
    my_file = os.path.join(file_dir, 'main_html_text.txt')

    try:
        with open(my_file, mode="w+", encoding=file_encoding) as file:
            file.writelines(src)
    except FileNotFoundError:
        logging.warning("Не удалось создать файл.", exc_info=None)

    end = process_time()
    logging.info(f"Текст был добавлен в файл по пути {my_file}, заняло: {end - start} времени.")


def count_of_vacancies():
    # vacancy - взял условно за одну вакансию, нашел одну строку совпадение в txt = одна вакансия
    vacancy: list[str] = ['Backend', 'Django']
    stop_point: str = "Выберите"

    try:
        with open('txt_here/main_html_text.txt', mode='r', encoding='utf-8') as file:
            for line in file:
                one_string_in_file: str = line
                if vacancy[0] in one_string_in_file or vacancy[1] in one_string_in_file:
                    write_status_indicator()
                    logging.info(f'Была найдена вакансия. Записали индикатор \'1\' в file в  dir: tg_bot')

                if stop_point in one_string_in_file:
                    break
    except FileNotFoundError:
        logging.warning("Файла нет в системе.", exc_info=None)

    logging.info(f'Вакансии еще нет.')


def write_status_indicator() -> None:
    # Записать '1' в status_indicator.txt
    path: str = os.getcwd() + r'\tg_bot\status_indicator.txt'
    try:
        with open(path, mode='w+', encoding='utf-8') as file:
            file.write('1')
            sys.exit()
    except FileNotFoundError:
        logging.warning("Не удалось записать '1' в файл.", exc_info=None)


def main():
    set_logging_settings()
    while True:
        retrieve_request_text()
        count_of_vacancies()
        r = random.randint(1, 61)
        time.sleep(1178 + r)


if __name__ == "__main__":
    main()
