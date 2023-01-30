import datetime
from git import Repo
import os
import platform
import time
import gc

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Rodar 1 vez ou em loop
opcao = input("1- Executar uma vez.\n2- Executar em loop.\n")

if opcao == '1':
    i = 1
    intervalo = 1
elif opcao == '2':
    i = 2
    intervalo = 600  # 14400s = 4h / 7200s = 2h / 3600s = 1h
else:
    print('Fechando...')
    quit()

# URL's
url_acoes = 'https://tinyurl.com/3s2xy5z3'
url_fiis = 'https://tinyurl.com/yck5nfd4'

# Pasta de download
full_path = os.path.realpath(__file__)
download_folder = (os.path.dirname(full_path))
print(f'O arquivo será salvo em {download_folder}')

# Chrome
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
servico = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Headless mode
chrome_options.add_argument(f"user-agent={user_agent}")  # Agent
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

prefs = {f"download.default_directory": f"{download_folder}"}
chrome_options.add_experimental_option("prefs", prefs)
navegador = webdriver.Chrome(service=servico, options=chrome_options)

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

def baixar_csv_fiis():

    # Baixando o csv de FIIs
    print("Baixando FII's...")
    navegador.get(f'{url_fiis}')
    time.sleep(5)

    # Renomeando o csv de FIIs
    original = 'statusinvest-busca-avancada.csv'
    correto = 'dadosfiis.csv'
    os.remove('dadosfiis.csv')
    os.rename(original, correto)
    print(f" O arquivo {original} foi renomeado para {correto}")


def baixar_csv_acoes():

    # Baixando o csv de ações
    print("Baixando Ações...")
    navegador.get(f'{url_acoes}')
    time.sleep(5)

    # Renomeando o csv de ações
    original = 'statusinvest-busca-avancada.csv'
    correto = 'dadosacoes.csv'
    os.remove('dadosacoes.csv')
    os.rename(original, correto)
    print(f" O arquivo {original} foi renomeado para {correto}")


def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        print('Push: OK.')
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
[Ações - .csv](https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/dadosacoes.csv) <br>
[FII's - Googlesheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vS97G13-9owVwSm1y_TAE3gTaxYflhMvgXCYgj3zEGVwqrbPiUrsOyUUcdhM5D7YVJPNaiinn51Plgc/pubhtml?gid=1741348998&single=true) <br>
[FII's - .csv](https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/dadosfiis.csv) <br>


Exemplo de uso no Googlesheets:
```sh
=IMPORTDATA("https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/dadosacoes.csv";";";"pt_BR")
```

![img_2.png](exemplo.png)

"""
    
    leitor = open("README.md", "w")  # encoding="cp1252" testar
    leitor.write(readme_conteudo)
    leitor.close()
    print('Readme.md: OK.')


# Atualizar tudo
def atualizar():
    last_update = datetime.datetime.now().strftime("%d/%m/%Y ás %H:%M:%S")
    baixar_csv_fiis()
    baixar_csv_acoes()
    criar_readme()
    git_push()
    print('Auto update: OK.')
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
        print('Encerrando...')
        navegador.quit()
        quit()


while True:
    loop()
