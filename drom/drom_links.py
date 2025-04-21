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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

service = Service('C:/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://auto.drom.ru/used/all/"

all_ad_links = []

num_pages = 1

driver.get(url)

for page in range(num_pages):
    print(f"Парсинг страницы {page + 1}...")

    try:
        wait = WebDriverWait(driver, 10)
        ad_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-ftid="bull_title"]')))
    except Exception as e:
        print(f"Ошибка при загрузке элементов на странице {page + 1}: {e}")
        ad_elements = []

    ad_links = [ad.get_attribute('href') for ad in ad_elements if ad.get_attribute('href')]
    all_ad_links.extend(ad_links)

    print(f"Найдено {len(ad_links)} ссылок на странице {page + 1}.")

    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-ftid="component_pagination-item-next"]')))
        next_button.click()
        time.sleep(1)
    except Exception as e:
        print(f"Не удалось перейти на следующую страницу: {e}")
        break

driver.quit()

with open('drom_links.json', 'w', encoding='utf-8') as f:
    json.dump(all_ad_links, f, ensure_ascii=False, indent=4)

print(f"Собрано {len(all_ad_links)} ссылок на объявления.")