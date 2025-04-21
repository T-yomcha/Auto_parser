from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

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

while len(links) < 50:
    driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
    i += 1
    time.sleep(scroll_pause_time)

    elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/moskva/auto/']")
    for elem in elements:
        href = elem.get_attribute("href")
        if href:
            links.add(href)
        if len(links) >= 100:
            break

with open("youla_links.json", "w") as f:
    json.dump(list(links), f, ensure_ascii=False, indent=4)
print(f"Собрано {len(links)} ссылок.")

driver.quit()