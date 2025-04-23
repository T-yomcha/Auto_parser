from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

def collect_avito_links():
    service = ChromeService(executable_path="C:/chromedriver-win64/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    base_url = "https://www.avito.ru/all/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?p="
    links_set = set()

    num_pages = 3

    for page in range(1, num_pages + 1):
        url = base_url + str(page)
        print(f"Обработка страницы {page}...")

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-marker='item']"))
            )
            time.sleep(1)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            listings = soup.find_all("div", {"data-marker": "item"})
            print(f"Страница {page}: Найдено объявлений: {len(listings)}")

            for item in listings:
                link_tag = item.find("a", {"data-marker": "item-title"})
                link = "https://www.avito.ru" + link_tag["href"] if link_tag else None

                if link and link not in links_set:
                    links_set.add(link)

        except Exception as e:
            print(f"Ошибка на странице {page}: {str(e)}")
            continue

    with open("avito_links.json", "w", encoding="utf-8") as f:
        json.dump(list(links_set), f, ensure_ascii=False, indent=4)
    print("Ссылки сохранены в avito_links.json")

    driver.quit()