import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_autoru_data():
    service = ChromeService(executable_path="C:/chromedriver-win64/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=options)

    with open("autoru_links.json", "r", encoding="utf-8") as f:
        links = json.load(f)

    cars_data = []

    for link in links:
        print(f"Обработка: {link}")
        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[@class='CardHead__title']")))
            time.sleep(1)

            try:
                title = driver.find_element(By.XPATH, "//h1[@class='CardHead__title']").text.strip()
            except:
                title = "Не указано"

            try:
                price = driver.find_element(By.XPATH,
                                            "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span/span").text.strip()
            except:
                price = "Не указано"

            try:
                description = driver.find_element(By.XPATH,
                                                  "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[7]/div[2]/div/div[1]/div/div/span").text.strip()
            except:
                description = "Не указано"

            try:
                engine_type = driver.find_element(By.XPATH,
                                                  "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[5]/div[1]/div[2]/ul[1]/li[7]/div[2]/div").text.strip()
            except:
                engine_type = "Не указано"

            try:
                body_type = driver.find_element(By.XPATH,
                                                "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[5]/div[1]/div[2]/ul[1]/li[5]/div[2]/a").text.strip()
            except:
                body_type = "Не указано"

            try:
                transmission = driver.find_element(By.XPATH,
                                                   "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[5]/div[1]/div[2]/ul[1]/li[10]/div[2]").text.strip()
            except:
                transmission = "Не указано"

            try:
                drive_type = driver.find_element(By.XPATH,
                                                 "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[5]/div[1]/div[2]/ul[1]/li[11]/div[2]").text.strip()
            except:
                drive_type = "Не указано"

            try:
                mileage = driver.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[5]/div[1]/div[2]/ul[1]/li[4]/div[2]").text.strip()
            except:
                mileage = "Не указано"

            try:
                location = driver.find_element(By.CLASS_NAME, "MetroListPlace__regionName").text.strip()
            except:
                location = "Не указано"

            try:
                date_public = driver.find_element(By.XPATH,
                                                  "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div[1]").text.strip()
            except:
                date_public = "Не указано"

            cars_data.append({
                "title": title,
                "price": price,
                "description": description,
                "engine_type": engine_type,
                "body_type": body_type,
                "drive_type": drive_type,
                "transmission": transmission,
                "mileage": mileage,
                "location": location,
                "publication_date": date_public,
                "link": link
            })

            time.sleep(1)

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            continue

    driver.quit()

    with open("autoru_data.json", "w", encoding="utf-8") as f:
        json.dump(cars_data, f, ensure_ascii=False, indent=4)

    print("Данные сохранены в autoru_data.json")