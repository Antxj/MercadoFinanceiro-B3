import time
import pandas as pd
import requests
import datetime
from ischedule import schedule, run_loop
import fontedados  # gitignore na fonte dos dados.
from git import Repo
import os
import platform

# Intervalo atualização
intervalo = 1  # 14400s = 4h / 7200s = 2h
agora = datetime.datetime.now()
last_update = agora.strftime("%d-%m-%Y ás %H:%M:%S")
import conteudo

# Pastas .git do repositório
PATH_OF_GIT_REPO_WIN = os.getcwd() + '\.git'
PATH_OF_GIT_REPO_LINUX = os.getcwd() + '/.git'

# Checando Sistema Operacional
my_os = platform.system()  # Windows / Linux

if my_os == 'Windows':
    print(f'Sistema Operacional: {my_os}')
    PATH_OF_GIT_REPO = PATH_OF_GIT_REPO_WIN
elif my_os == 'Linux':
    print(f'Sistema Operacional: {my_os}')
    PATH_OF_GIT_REPO = PATH_OF_GIT_REPO_LINUX
else:
    print(f'Sistema Operacional {my_os} não identificado.')
    exit()


# Auto push Github
COMMIT_MESSAGE = f'PI4: Auto update {intervalo/60:.2f} minutos'


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


# Criar README.md
def criar_readme():
        leitura = open("README.md", "w", encoding="cp1252")
        leitura.write(conteudo.readme_conteudo)


def atualizar():
    # Baixando o arquivos .csv
    response = requests.get(fontedados.url_acoes)
    open("resultado/dadosacoes.csv", "wb").write(response.content)
    response = requests.get(fontedados.url_fiis)
    time.sleep(2)
    open("resultado/dadosfiis.csv", "wb").write(response.content)
    time.sleep(2)

    # Lendo e salvando os arquivos .csv
    pd.read_csv(r'resultado/dadosacoes.csv', sep=";", decimal='.')
    pd.read_csv(r'resultado/dadosfiis.csv', sep=";", decimal='.')

    # Quando executou
    agora = datetime.datetime.now()
    last_update = agora.strftime("%d-%m-%Y ás %H:%M:%S")

    # Csv -> Html table (TO DO)
    # file = pd.read_csv('resultado/dadosacoes.csv', sep=";", decimal='.')
    # file.to_html("html/tabelaacoes.html")
    # file = pd.read_csv('resultado/dadosfiis.csv', sep=";", decimal='.')
    # file.to_html("html/tabelafiis.html")

    # Push
    git_push()

    print(f'Atualização a cada {intervalo / 60:.2f} minutos')
    print(f'Última atualização: {last_update}.')



schedule(atualizar, interval=intervalo)
schedule(criar_readme, interval=intervalo)
run_loop()



