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

import etf
import tesouro
from fiiagro import fii_agro

# Rodar 1 vez ou em loop
opcao = input("1- Executar uma vez.\n2- Executar em loop.\n")

if opcao == '1':
    i = 1
    intervalo = 1
elif opcao == '2':
    i = 2
    intervalo = 3600  # 14400s = 4h / 7200s = 2h / 3600s = 1h
else:
    print('Fechando...')
    quit()

# Pasta de download
full_path = os.path.realpath(__file__)
download_folder = (os.path.dirname(full_path)) + "\csv"
print(f'O arquivo será salvo em {download_folder}')

# Chrome
# ua = UserAgent(browsers=['chrome'])
# user_agent = ua.random
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
# chrome_options.add_argument("--headless")  # Headless mode
servico = Service(ChromeDriverManager().install())
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

prefs = {f"download.default_directory": f"{download_folder}"}
chrome_options.add_experimental_option("prefs", prefs)
navegador = webdriver.Chrome(service=servico, options=chrome_options)

# URL's
url_acoes = 'https://statusinvest.com.br/category/AdvancedSearchResultExport?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%22-20%3B100%22%2C%22forecast%22%3A%7B%22upsideDownside%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22estimatesNumber%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22revisedUp%22%3Atrue%2C%22revisedDown%22%3Atrue%2C%22consensus%22%3A%5B%5D%7D%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22peg_Ratio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22vpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorMercado%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=1'
url_fiis = 'https://statusinvest.com.br/category/AdvancedSearchResultExport?search=%7B%22Segment%22%3A%22%22%2C%22Gestao%22%3A%22%22%2C%22my_range%22%3A%220%3B20%22%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_vp%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22percentualcaixa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22numerocotistas%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividend_cagr%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22cota_cagr%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezmediadiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22patrimonio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorpatrimonialcota%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22numerocotas%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lastdividend%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=2'
url_stocks = 'https://statusinvest.com.br/category/AdvancedSearchResultExport?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%22-20%3B100%22%2C%22forecast%22%3A%7B%22upsideDownside%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22estimatesNumber%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22revisedUp%22%3Atrue%2C%22revisedDown%22%3Atrue%2C%22consensus%22%3A%5B%5D%7D%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22peg_Ratio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22vpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorMercado%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=12'
url_reits = 'https://statusinvest.com.br/category/AdvancedSearchResultExport?search=%7B%22Segment%22%3A%22%22%2C%22my_range%22%3A%22-20%3B100%22%2C%22forecast%22%3A%7B%22upsideDownside%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22estimatesNumber%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22revisedUp%22%3Atrue%2C%22revisedDown%22%3Atrue%2C%22consensus%22%3A%5B%5D%7D%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22peg_Ratio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22vpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorMercado%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=13'

# Intervalo atualização
# intervalo = 600  # 14400s = 4h / 7200s = 2h / 3600s = 1h
last_update = datetime.datetime.now().strftime("%d/%m/%Y ás %H:%M:%S")
     
# Pasta .git e python de acordo com o OS
my_os = platform.system()  # Windows / Linux

if my_os == 'Windows':
    PATH_OF_GIT_REPO = os.getcwd() + '\.git'  # Pastas .git do repositório no Windows
    print(f'{my_os} identificado.')
elif my_os == 'Linux':
    PATH_OF_GIT_REPO = os.getcwd() + '/.git'  # Pastas .git do repositório no Linux
    print(f'{my_os} identificado.')
else:
    print(f'Sistema Operacional {my_os} não identificado.')
    exit()

# Auto push no Github
COMMIT_MESSAGE = f'PI4: Auto update em: {intervalo / 60:.2f} minutos'

# Baixando os arquivos .csv


def get_csv_rename(url, nome):
    navegador.get(f'{url}')
    time.sleep(3)

    # Renomeando ultimo csv
    lista_arquivos = glob.glob(download_folder + '\*')
    ultimo_arquivo = max(lista_arquivos, key=os.path.getmtime)
    os.remove(f'csv\{nome}')
    os.rename(ultimo_arquivo, f'csv\{nome}')
    print(f"{nome} - OK.")


def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        print('Push - OK.')
    except:
        print('Deu erro na hora do push!')


# Criando README.md
def criar_readme():
    last_update = datetime.datetime.now().strftime("%d/%m/%Y ás %H:%M:%S")
    # README.MD
    readme_conteudo = f"""
# StatusInvest - Dados
Informações das Ações e dos FII's listados na StatusInvest atualizadas a cada {intervalo / 60:.2f} minutos rodando em um [Raspberry Pi 4 Model B](https://www.raspberrypi.com/) que estava parado.

Atualização automática em: {intervalo / 60:.2f} minutos. <br>
<br>Última atualização: {last_update}.  <br>


>Resultados: <br>
[Ações - Googlesheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vS97G13-9owVwSm1y_TAE3gTaxYflhMvgXCYgj3zEGVwqrbPiUrsOyUUcdhM5D7YVJPNaiinn51Plgc/pubhtml?gid=313887204&single=true) <br>
[Ações - .csv](https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/csv/dadosacoes.csv) <br>
[FII's - Googlesheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vS97G13-9owVwSm1y_TAE3gTaxYflhMvgXCYgj3zEGVwqrbPiUrsOyUUcdhM5D7YVJPNaiinn51Plgc/pubhtml?gid=1741348998&single=true) <br>
[FII's - .csv](https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/csv/dadosfiis.csv) <br>


Exemplo de uso no Googlesheets:
```sh
=IMPORTDATA("https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/csv/dadosacoes.csv";";";"pt_BR")
```

![img_2.png](exemplo.png)

"""
    
    leitor = open("README.md", "w")  # encoding="cp1252" testar
    leitor.write(readme_conteudo)
    leitor.close()
    print('Readme.md - OK.')


# Atualizar tudo
def atualizar():
    last_update = datetime.datetime.now().strftime("%d/%m/%Y ás %H:%M:%S")
    get_csv_rename(url_fiis, 'dadosfiis.csv')
    get_csv_rename(url_acoes, 'dadosacoes.csv')
    get_csv_rename(url_stocks, 'dadosstocks.csv')
    get_csv_rename(url_reits, 'dadosreits.csv')
    etf.etf_eua()
    tesouro.tesouro()
    fii_agro()
    criar_readme()
    git_push()
    navegador.quit()

    print('Auto update - OK.')
    print(f'Atualização a cada {intervalo / 60:.2f} minutos')
    print(f'Última atualização: {last_update}.')

    collected = gc.collect()
    print("Garbage collector: collected",
          "%d objects." % collected)


# Rodar em loop
# i = 0


def loop():
    global i
    print(f' ###### Execução nº: {i - 1} ######')
    i += 1
    time.sleep(intervalo)
    atualizar()
    if i == 2:
        navegador.quit()
        quit()
        print('Finalizado.')


while True:
    loop()
    