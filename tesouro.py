import csv
import os
import time

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Chrome
servico = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Headless mode
ua = UserAgent(browsers=['chrome'])
user_agent = ua.random
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
# chrome_options.add_argument(rf'--user-data-dir={path_chrome}')  # Funciona mas expira e dá trabalho.
chrome_options.add_argument(f"user-agent={user_agent}")  # Agent
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
navegador = webdriver.Chrome(service=servico, options=chrome_options)

# os.remove("csv\\tesouro.csv")


# Tesouro
def tesouro():
    def valor_tesouro(tesouro):
        url = f'https://statusinvest.com.br/tesouro/{tesouro}/'
        navegador.get(f'{url}')
        dado = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="tesouro"]/div/div[1]/div/div[1]/div/div[1]/strong'))).get_attribute("innerHTML")
        dado = dado.replace('R$ ', '')
        dado = " ".join(line.strip() for line in dado.splitlines())
        dado = dado.replace(' ', '')
        print(f'{tesouro} - {dado}')
        with open("csv\\tesouro.csv", 'a+', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            infos = [f'{tesouro}', f'{dado}']
            writer.writerow(infos)

    tickers_fiisagro = ['tesouro-prefixado-2025']

    for i in tickers_fiisagro:
        valor_tesouro(i)
        time.sleep(1)

    navegador.quit()
    print('Tesouro - OK.')
