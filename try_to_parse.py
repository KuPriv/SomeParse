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
    req = requests.get("https://prodoctorov.ru/krasnodar/vrach/", get_headers_for_request())
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
        # TODO? по идее, еще должна быть одна ошибка, но пока пусть будет так.
        logging.warning("Не удалось создать файл.", exc_info=None)

    end = process_time()
    logging.info(f"Текст был добавлен в файл по пути {my_file}, заняло: {end - start} времени.")


def main():
    set_logging_settings()
    retrieve_request_text()

if __name__ == "__main__":
    main()
