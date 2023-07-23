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

os.remove('csv\dyoc.csv')

# FII's AGRO
def dy_ano_fiisagro(ticker):
    url = f'https://statusinvest.com.br/fiagros/{ticker}/'
    navegador.get(f'{url}')
    dado = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="main-2"]/div[2]/div[1]/div[4]/div/div[2]/div/span[2]'))).get_attribute("innerHTML")
    dado = dado.replace('R$ ', '')
    dado = " ".join(line.strip() for line in dado.splitlines())
    dado = dado.replace(' ', '')
    print(f'{ticker} - {dado}')
    with open('csv\dyoc.csv', 'a+', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        infos = [f'{ticker}', f'{dado}']
        writer.writerow(infos)


tickers_fiisagro = ['SNAG11', 'KNCA11', 'RZAG11']

for i in tickers_fiisagro:
    dy_ano_fiisagro(i)
    time.sleep(1)


# ETF
def dy_ano_etfs(ticker):
    url = f'https://stockanalysis.com/etf/{ticker}/dividend/'
    navegador.get(f'{url}')
    dado = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[2]/div'))).get_attribute("innerHTML")
    dado = dado.replace('$', '')
    dado = dado.replace('.', ',')
    print(f'{ticker} - {dado}')
    with open('csv\dyoc.csv', 'a+', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        infos = [f'{ticker}', f'{dado}']
        writer.writerow(infos)


tickers_etfs = ['VOO', 'VNQ', 'VNQI', 'PGX', 'LQD', 'SCHD', 'NOBL']
for i in tickers_etfs:
    dy_ano_etfs(i)
    time.sleep(1)


# FII's
def dy_ano_fiis(ticker):
    url = f'https://statusinvest.com.br/fundos-imobiliarios/{ticker}/'
    navegador.get(f'{url}')
    dado = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="main-2"]/div[2]/div[1]/div[4]/div/div[2]/div/span[2]'))).get_attribute("innerHTML")
    dado = dado.replace('R$ ', '')
    print(f'{ticker} - {dado}')
    with open('csv\dyoc.csv', 'a+', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        infos = [f'{ticker}', f'{dado}']
        writer.writerow(infos)


tickers_fiis = ['BCFF11', 'HFOF11', 'HSML11', 'LGCP11', 'HOFC11', 'VILG11', 'MXRF11', 'RECR11', 'BTAL11',
                'KNCR11', 'XPPR11', 'TGAR11', 'HGRU11', 'HGLG11', 'GGRC11', 'TRBL11', 'XPML11', 'VISC11',
                'KFOF11']

for i in tickers_fiis:
    dy_ano_fiis(i)
    time.sleep(1)


# Acoes
def dy_ano_acoes(ticker):
    url = f'https://statusinvest.com.br/acoes/{ticker}'
    navegador.get(f'{url}')
    dado = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[4]/div/div[2]/div/span[2]'))).get_attribute("innerHTML")
    dado = dado.replace('R$ ', '')
    print(f'{ticker} - {dado}')
    with open('csv\dyoc.csv', 'a+', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        infos = [f'{ticker}', f'{dado}']
        writer.writerow(infos)


tickers_acoes = ['ITSA4', 'BBDC4', 'EGIE3', 'AESB3', 'TAEE11', 'TASA4', 'KLBN4', 'SAPR4', 'WIZC3', 'ALUP11', 'PETR4']
for i in tickers_acoes:
    dy_ano_acoes(i)
    time.sleep(1)

print("""
--------------
DYOC concluído.
--------------
""")
navegador.quit()
