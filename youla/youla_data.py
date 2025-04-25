import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def parse_youla_data():
    """Парсит детальную информацию об автомобилях с сайта по сохраненным ссылкам.

    Функция загружает список ссылок из файла json, последовательно посещает
    каждую страницу с объявлением и извлекает следующие данные:
    - Название автомобиля
    - Цену
    - Описание
    - Тип двигателя
    - Тип кузова
    - Тип привода
    - Коробку передач
    - Пробег
    - Местоположение
    - Дату публикации
    - Ссылку на объявление

    Args:
        Нет аргументов.

    Returns:
        None: Функция не возвращает значений, но сохраняет результаты в файл.

    Raises:
        FileNotFoundError: Если файл json не найден.
        JSONDecodeError: Если файл json содержит некорректный JSON.
        WebDriverException: При ошибках работы Selenium WebDriver.
        Exception: Другие возможные исключения при парсинге.

    Notes:
        - Использует headless-режим браузера Chrome.
        - Добавляет задержки между запросами для имитации человеческого поведения.
        - Обрабатывает случаи отсутствия данных, заменяя их на "Не указано".
        - Сохраняет данные в формате JSON с сохранением кириллических символов.

    Examples:
        >>> parse_youla_data()
        Обработка: https://auto.ru/cars/used/sale/.../
        Обработка: https://auto.ru/cars/used/sale/.../
        Данные сохранены в json
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("C:/chromedriver-win64/chromedriver.exe")

    with open("youla_links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    cars_data = []

    def get_text_by_xpath(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return "Не указано"

    def get_text_by_css(selector):
        try:
            return driver.find_element(By.CSS_SELECTOR, selector).text.strip()
        except:
            return "Не указано"

    for link in links:
        driver.get(link)
        print(f"Обработка: {link}")
        try:
            wait = WebDriverWait(driver, 5)

            try:
                show_more_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Все параметры')]")
                show_more_button.click()
                time.sleep(1)
            except:
                pass

            def get_publication_date():
                try:
                    publication_date_label = driver.find_element(By.XPATH, "//dt[contains(text(), 'Размещено')]")
                    publication_date = publication_date_label.find_element(By.XPATH,
                                                                           "following-sibling::dd").text.strip()
                    return publication_date
                except:
                    return "Не указано"

            car_data = {
                "title": get_text_by_css('h2[data-test-block="ProductCaption"]'),
                "price": get_text_by_css('span.sc-fxhZON.fzJDlO'),
                "year": get_text_by_xpath("//dt[contains(text(), 'Год выпуска')]/following-sibling::dd"),
                "power": get_text_by_xpath("//dt[contains(text(), 'Мощность')]/following-sibling::dd"),
                "fuel": get_text_by_xpath("//dt[contains(text(), 'Тип двигателя')]/following-sibling::dd"),
                "engine_volume": get_text_by_xpath("//dt[contains(text(), 'Объем двигателя')]/following-sibling::dd"),
                "transmission": get_text_by_xpath("//dt[contains(text(), 'Коробка передач')]/following-sibling::dd"),
                "mileage": get_text_by_xpath("//dt[contains(text(), 'Пробег')]/following-sibling::dd"),
                "body_type": get_text_by_xpath("//dt[contains(text(), 'Кузов')]/following-sibling::dd"),
                "drive_type": get_text_by_xpath("//dt[contains(text(), 'Привод')]/following-sibling::dd"),
                "description": get_text_by_xpath("//dt[contains(text(), 'Описание')]/following-sibling::dd"),
                "location": get_text_by_xpath("//dt[contains(text(), 'Местоположение')]/following-sibling::dd"),
                "publication_date": get_publication_date(),
                "link": link
            }

            cars_data.append(car_data)

        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")
            continue

    with open("youla_data.json", "w", encoding="utf-8") as f:
        json.dump(cars_data, f, ensure_ascii=False, indent=4)
    print("Данные сохранены в youla_data.json")

    driver.quit()