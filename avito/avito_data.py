import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_avito_data():
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
        >>> parse_avito_data()
        Обработка: https://auto.ru/cars/used/sale/.../
        Обработка: https://auto.ru/cars/used/sale/.../
        Данные сохранены в json
    """
    def get_car_param(param_name):
        try:
            elements = driver.find_elements(By.XPATH, "//li")
            for elem in elements:
                if param_name in elem.text:
                    return elem.text.replace(param_name, "").strip()
        except:
            pass
        return "Не указано"

    try:
        with open("avito_links.json", "r", encoding="utf-8") as f:
            links = json.load(f)
        print(f"Успешно загружено {len(links)} ссылок из avito_links.json")
    except Exception as e:
        print(f"Ошибка при чтении файла avito_links.json: {str(e)}")
        links = []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service("C:/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    cars_data = []

    if not links:
        print("Список ссылок пуст. Завершаем работу.")
    else:
        for link in links:
            print(f"Обработка: {link}")
            try:
                driver.get(link)

                title = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@itemprop='name']"))
                ).text.strip()

                try:
                    price = driver.find_element(By.XPATH,
                                                "/html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div/span/span/span[1]").text.strip()
                except:
                    price = "Не указано"

                try:
                    description = driver.find_element(By.XPATH,
                                                      "//div[@data-marker='item-view/item-description']").text.strip()
                except:
                    description = "Не указано"

                engine_type = get_car_param("Тип двигателя:")
                drive_type = get_car_param("Привод:")
                body_type = get_car_param("Тип кузова:")
                transmission = get_car_param("Коробка передач:")

                try:
                    location = driver.find_element(By.XPATH,
                                                   "/html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[4]/div/div[1]/div[1]/div/span").text.strip()
                except:
                    location = "Не указано"

                try:
                    publication_date = driver.find_element(By.XPATH,
                                                           "//span[@data-marker='item-view/item-date']").text.strip()
                except:
                    publication_date = "Не указано"

                cars_data.append({
                    "title": title,
                    "price": price,
                    "description": description,
                    "engine_type": engine_type,
                    "body_type": body_type,
                    "drive_type": drive_type,
                    "transmission": transmission,
                    "location": location,
                    "publication_date": publication_date,
                    "link": link
                })

                time.sleep(1)

            except Exception as e:
                print(f"Ошибка при обработке {link}: {str(e)}")
                continue

    with open("avito_data.json", "w", encoding="utf-8") as f:
        json.dump(cars_data, f, ensure_ascii=False, indent=4)

    print("Данные сохранены в avito_data.json")
    driver.quit()
