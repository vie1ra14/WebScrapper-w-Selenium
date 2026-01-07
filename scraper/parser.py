from selenium.webdriver.common.by import By

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

    return {
        "title": title,
        "company": company,
        "location": location
    }
