import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

service = Service('C:/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

with open("drom_links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

cars_data = []

for link in links:
    print(f"Обработка: {link}")
    try:
        driver.get(link)
        wait = WebDriverWait(driver, 5)

        try:
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1 span.css-1kb7l9z"))).text.strip()
        except:
            title = "Не указано"

        try:
            price = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[1]").text.strip()
        except:
            price = "Не указано"

        try:
            description = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/span[2]").text.strip()
        except:
            description = "Не указано"

        try:
            location = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[4]/div[2]").text.strip()
        except:
            location = "Не указано"

        try:
            publication_date = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[1]/div[4]/div/div[1]").text.strip()
        except:
            publication_date = "Не указано"

        try:
            engine = driver.find_element(By.CSS_SELECTOR, "td.css-1azz3as.eka0pcn0").text.strip()
        except:
            engine = "Не указано"

        try:
            transmission = driver.find_element(By.XPATH, "//th[contains(text(), 'Коробка передач')]/following-sibling::td").text.strip()
        except:
            transmission = "Не указано"

        try:
            mileage = driver.find_element(By.XPATH, "//th[contains(text(), 'Пробег')]/following-sibling::td").text.strip()
        except:
            mileage = "Не указано"

        try:
            power = driver.find_element(By.CSS_SELECTOR, "span.css-gy2hs8.e162wx9x0").text.split()[0]
        except:
            power = "Не указано"

        try:
            body_type = driver.find_element(By.XPATH, "//th[contains(text(), 'Кузов')]/following-sibling::td").text.strip()
        except:
            body_type = "Не указано"

        try:
            drive_type = driver.find_element(By.XPATH, "//th[contains(text(), 'Привод')]/following-sibling::td").text.strip()
        except:
            drive_type = "Не указано"

        cars_data.append({
            "title": title,
            "price": price,
            "description": description,
            "engine": engine,
            "transmission": transmission,
            "mileage": mileage,
            "power": power,
            "body_type": body_type,
            "drive_type": drive_type,
            "location": location,
            "publication_date": publication_date,
            "link": link
        })

    except Exception as e:
        print(f"Ошибка при обработке {link}: {e}")
        continue

driver.quit()

with open("drom_data.json", "w", encoding="utf-8") as f:
    json.dump(cars_data, f, ensure_ascii=False, indent=4)

print("Данные сохранены в drom_data.json")
