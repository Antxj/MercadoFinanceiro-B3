import csv
import os
import time

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Chrome
ua = UserAgent(browsers=['chrome'])
user_agent = ua.chrome
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

chromedriver_path = 'chromedriver.exe'
servico = ChromeService(executable_path=chromedriver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agent}")  # User Agent
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")  # Headless mode
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


def fii_agro():
    os.remove('csv\\fiiagro.csv')

    with open('csv\\fiiagro.csv', 'a+', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        index = ['Ticker', 'DY', 'DY_year', 'P/VP', 'Dividendo']
        writer.writerow(index)

    # Dados
    def fiiagro(ticker):
        url = f'https://statusinvest.com.br/fiagros/{ticker}'
        navegador.get(f'{url}')

        dy = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main-2"]/div[2]/div[1]/div[4]/div/div[1]/strong'))).get_attribute("innerHTML")

        dy_year = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main-2"]/div[2]/div[1]/div[4]/div/div[2]/div/span[2]'))).get_attribute("innerHTML")
        dy_year = dy_year.replace('R$ ', '')
        dy_year = " ".join(line.strip() for line in dy_year.splitlines())
        dy_year = dy_year.replace(' ', '')

        p_vp = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main-2"]/div[2]/div[4]/div/div[2]/div/div[1]/strong'))).get_attribute("innerHTML")

        dividendo = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="dy-info"]/div/div[1]/strong'))).get_attribute("innerHTML")

        # print(f'{ticker} - DY: {dy}% - DY_year: {dy_year} - P/VP: {p_vp} - Dividendo: {dividendo}')

        with open('csv\\fiiagro.csv', 'a+', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            infos = [f'{ticker}', f'{dy}', f'{dy_year}', f'{p_vp}', f'{dividendo}']
            writer.writerow(infos)

    tickers_fiiagro = ['SNAG11', 'KNCA11', 'RZAG11']
    for i in tickers_fiiagro:
        fiiagro(i)
        time.sleep(1)

    print("fiiagro.csv - OK")
