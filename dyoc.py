import time
from fake_useragent import UserAgent
import os
import json
import pandas as pd
import csv
import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Pasta de download
full_path = os.path.realpath(__file__)
download_folder = (os.path.dirname(full_path))
# print(f'O arquivo será salvo em {download_folder}')

# Caminho Chrome data
# user_pc = os.getlogin()
# path_chrome = fr'C:\Users\{user_pc}\AppData\Local\Google\Chrome\User Data\Default'

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
prefs = {f"download.default_directory": f"{download_folder}"}
chrome_options.add_experimental_option("prefs", prefs)


def dy_ano_acoes(ticker):
    url = f'https://statusinvest.com.br/acoes/{ticker}'
    navegador.get(f'{url}')
    dado = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[4]/div/div[2]/div/span[2]'))).get_attribute("innerHTML")
    dado = dado.replace('R$ ', '')
    print(f'{ticker} - {dado}')


tickers_acoes = ['ITSA4', 'BBDC4', 'EGIE3', 'AESB3', 'TAEE11', 'TASA4', 'KLBN4', 'SAPR4', 'WIZC3']
for i in tickers_acoes:
    dy_ano_acoes(i)

