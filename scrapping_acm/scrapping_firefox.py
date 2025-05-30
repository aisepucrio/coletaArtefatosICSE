from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

icse_proceedings = {
    2024:'https://dl.acm.org/doi/proceedings/10.1145/3597503',
    2023:'https://dl.acm.org/doi/proceedings/10.5555/3606010',
    2022:'https://dl.acm.org/doi/proceedings/10.1145/3510003', 
    2021:'https://dl.acm.org/doi/proceedings/10.5555/3498096',
    2020:'https://dl.acm.org/doi/proceedings/10.1145/3377811',
    2019:'https://dl.acm.org/doi/proceedings/10.5555/3339505'
}

gecko_driver_path = r"C:\Users\guicu\OneDrive\Documentos\firefox-driver\geckodriver.exe"

def open_close_session(elemento,heading_id):
    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, heading_id))
        )
        elemento.click()
        if elemento.get_attribute("aria-expanded") == "true":
            print("Expanded successfully.")
        else:
            print("Deexpanded successfully.")
    except Exception:
        print("Faield to expand or deexpand the session.")

def get_metadata(year):
    articles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'issue-item-container')))
    print(f"{len(articles)} articles found.")

    results = []

    for article in articles:
        try:
            title_element = article.find_element(By.CSS_SELECTOR, '.issue-item__title a')
            title = title_element.get_attribute('innerText').strip()
            doi = title_element.get_attribute('href')
        except:
            title = "Title not found"
            doi = "DOI not found"

        artifact_available = False
        artifact_reusable = False
        artifact_functional = False
        try:
            badges_div = article.find_element(By.CLASS_NAME, 'badges')
            badge_imgs = badges_div.find_elements(By.CSS_SELECTOR, '.img-badget img')
            for img in badge_imgs:
                alt_text = img.get_attribute("alt")
                if alt_text == "Artifacts Available / v1.1":
                    artifact_available = True
                elif alt_text == "Artifacts Evaluated & Reusable / v1.1":
                    artifact_reusable = True
                elif alt_text == "Artifacts Evaluated & Functional / v1.1":
                    artifact_functional = True
        except:
            pass

        result = {
            "Title": title,
            "DOI": doi,
            "Artifact Available": artifact_available,
            "Artifact Reusable": artifact_reusable,
            "Artifact Functional": artifact_functional
        }

        results.append(result)

        print("-" * 50)
        print("Title:", title)
        print("DOI:", doi)
        print("Artifact Available:", artifact_available)
        print("Artifact Reusable:", artifact_reusable)
        print("Artifact Functional:", artifact_functional)

    file_name= f"{year}acm_articles.csv"
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "DOI", "Artifact Available", "Artifact Reusable", "Artifact Functional"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Results saved in {file_name}")

def accept_cookies():
    try:
        accept_cookies = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        accept_cookies.click()
        print("Cookies accepted.")
        time.sleep(3)
    except:
        print("No cookie popup appeared.")

def load_sessions():
    num = 1 
    while True:
        heading_id = f"heading{num}"
        try:
            element = driver.find_element(By.ID, heading_id)
            if element.get_attribute("aria-expanded") != "true":
                open_close_session(element,heading_id)
                time.sleep(3)
            open_close_session(element,heading_id)
            num += 1
        except NoSuchElementException:
            print(f"ID '{heading_id}' do not appeared. All sessions loaded.")
            break

if __name__ == "__main__":
    for year, url in icse_proceedings.items():
        url= url

        firefox_options = Options()
        firefox_options.add_argument("--start-maximized")

        service = Service(executable_path=gecko_driver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)

        driver.get(url)

        wait = WebDriverWait(driver, 1)
        accept_cookies()
        load_sessions()
        get_metadata(year)
        print("Closing the browser...")
        driver.quit()
