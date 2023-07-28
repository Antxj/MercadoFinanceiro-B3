import csv
import os
import time

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Chrome
ua = UserAgent(browsers=['chrome'])
user_agent = ua.chrome
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# chrome_options.add_argument("--headless")  # Headless mode
chromedriver_path = 'chromedriver.exe'
servico = ChromeService(executable_path=chromedriver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agent}")  # User Agent
# chrome_options.add_argument("--incognito")
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


def etf_eua():
    os.remove('csv\etf.csv')

    with open('csv\etf.csv', 'a+', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        index = ['Ticker', 'DY', 'DY YEAR']
        writer.writerow(index)

    # ETF
    def etf(ticker):
        url = f'https://stockanalysis.com/etf/{ticker}/dividend/'
        navegador.get(f'{url}')
        dy_ano = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[2]/div'))).get_attribute("innerHTML")
        dy_ano = dy_ano.replace('$', '')
        dy_ano = dy_ano.replace('.', ',')

        dy = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[1]/div'))).get_attribute("innerHTML")
        dy = dy.replace('%', '')
        dy = dy.replace('.', ',')

        # print(f'{ticker} - DY: {dy}% - DY YEAR: ${dy_ano}')

        with open('csv\etf.csv', 'a+', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            infos = [f'{ticker}', f'{dy}', f'{dy_ano}']
            writer.writerow(infos)

    tickers_etfs = ['VOO', 'VNQ', 'VNQI', 'PGX', 'LQD', 'SCHD', 'NOBL']
    for i in tickers_etfs:
        etf(i)
        time.sleep(1)

    print('etf.csv - OK.')
