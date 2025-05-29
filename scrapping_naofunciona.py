from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

chrome_driver_path = r"C:\Users\guicu\OneDrive\Documentos\chrome-driver\chromedriver.exe" 
url_da_pagina = "https://dl.acm.org/doi/proceedings/10.1145/3597503"

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url_da_pagina)

wait = WebDriverWait(driver, 1)

def expande(elemento):
    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, heading_id))
        )
        elemento.click()
        print("Expandido com sucesso.")
    except Exception as e:
        print("Falha ao expandir")

def pega_metadados():
    containers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'issue-item-container')))
    print(f"Encontrados {len(containers)} blocos.")

try:
    aceitar_cookies = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
    )
    aceitar_cookies.click()
    print("Cookies aceitos.")
except:
    print("Popup de cookies não apareceu ou já estava fechado.")

num = 1
while True:
    heading_id = f"heading{num}"
    try:
        elemento = driver.find_element(By.ID, heading_id)
        #expande(elemento)
        time.sleep(200)
        #pega_metadados()
        #num += 1
    except NoSuchElementException:
        print(f"ID '{heading_id}' não encontrado. Encerrando loop.")
        break


