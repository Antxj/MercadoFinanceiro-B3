import datetime
from git import Repo
import os
import platform
import time
import gc
import requests
import pandas as pd
from fake_useragent import UserAgent
import glob

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Chrome
ua = UserAgent(browsers=['chrome'])
user_agent = ua.random
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'


servico = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Headless mode
chrome_options.add_argument(f"user-agent={user_agent}")  # User Agent
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

# URL's
url_acoes = 'https://tinyurl.com/3s2xy5z3'
url_fiis = 'https://tinyurl.com/yck5nfd4'
url_stocks = 'https://tinyurl.com/47s4j77h'
url_reits = 'https://tinyurl.com/ye2858s5'

# Pasta de download
full_path = os.path.realpath(__file__)
download_folder = (os.path.dirname(full_path)) + "\csv"
print(f'O arquivo será salvo em {download_folder}')

prefs = {f"download.default_directory": f"{download_folder}"}
chrome_options.add_experimental_option("prefs", prefs)
navegador = webdriver.Chrome(service=servico, options=chrome_options)


def get_csv_rename(url, nome):
    navegador.get(f'{url}')
    time.sleep(3)

    # Renomeando ultimo csv
    lista_arquivos = glob.glob(download_folder + '\*')
    ultimo_arquivo = max(lista_arquivos, key=os.path.getmtime)
    os.remove(f'csv\{nome}')
    os.rename(ultimo_arquivo, f'csv\{nome}')
    print(f" O arquivo {ultimo_arquivo} foi renomeado para {nome}")



# get_csv_rename(url_fiis, 'dadosfiis.csv')
# get_csv_rename(url_acoes, 'dadosacoes.csv')
# get_csv_rename(url_stocks, 'dadosstocks.csv')
# get_csv_rename(url_reits, 'dadosreits.csv')


