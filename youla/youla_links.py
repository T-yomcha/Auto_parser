from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

def collect_youla_links():
    """Собирает ссылки на объявления о продаже автомобилей с сайта.

    Функция использует Selenium WebDriver для парсинга страниц с объявлениями.
    Проходит по указанному количеству страниц, собирает все уникальные ссылки
    на объявления и сохраняет их в JSON-файл.

    Args:
        Нет аргументов.

    Returns:
        None: Функция не возвращает значений, но сохраняет результаты в файл.

    Raises:
        Exception: Могут возникать различные исключения Selenium при работе с веб-драйвером.
        IOError: При проблемах с сохранением файла.

    Notes:
        - Использует headless-режим браузера для фоновой работы.
        - Добавляет пользовательский user-agent для обхода защиты.
        - Сохраняет только уникальные ссылки (дубликаты игнорируются).
        - Включает задержки для имитации человеческого поведения.

    Examples:
        Обработка страницы 1...
        Страница 1: Найдено объявлений: 25
        Обработка страницы 2...
        Страница 2: Найдено объявлений: 25
        Ссылки сохранены в autoru_links.json
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-geolocation")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()

    driver.get("https://youla.ru/moskva/auto/s-probegom")

    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    links = set()

    while len(links) < 300:
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)
        time.sleep(1)

        elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/moskva/auto/']")
        for elem in elements:
            href = elem.get_attribute("href")
            if href:
                links.add(href)
            if len(links) >= 300:
                break

    with open("youla_links.json", "w") as f:
        json.dump(list(links), f, ensure_ascii=False, indent=4)
    print(f"Собрано {len(links)} ссылок.")

    driver.quit()

collect_youla_links()