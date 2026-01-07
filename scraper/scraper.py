import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from database.models import create_table, insert_job

URL = "https://www.indeed.com/jobs?q=python+developer&l="

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    return webdriver.Chrome(options=options)


def safe_find_text(element, selector, default="Desconhecido"):
    try:
        text = element.find_element(By.CSS_SELECTOR, selector).text.strip()
        return text if text else default
    except:
        return default

def parse_job_card(card):
    title = safe_find_text(card, "h2.jobTitle span", default="Sem título")
    company = safe_find_text(card, ".companyName", default="Desconhecida")
    location = safe_find_text(card, ".companyLocation", default="Desconhecida")
    return {"title": title, "company": company, "location": location}

def scrape_jobs():
    driver = get_driver()
    create_table()

    driver.get(URL)
    wait = WebDriverWait(driver, 20)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon")))
    except:
        driver.quit()
        return


    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")

    for card in cards:
        data = parse_job_card(card)
        insert_job(
            title=data["title"],
            company=data["company"],
            location=data["location"],
            collected_at=datetime.now()
        )

    driver.quit()

if __name__ == "__main__":
    scrape_jobs()
