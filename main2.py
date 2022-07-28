import pandas as pd
import requests
from ischedule import schedule, run_loop
import conteudo
import fontedados  # gitignore na fonte dos dados.
from git import Repo
import os
import platform

# Pasta .git de acordo com o OS
my_os = platform.system()  # Windows / Linux

if my_os == 'Windows':
    PATH_OF_GIT_REPO = os.getcwd() + '\.git'  # Pastas .git do repositório no Windows
    print(f'Pasta .git no {my_os}: {PATH_OF_GIT_REPO}')
elif my_os == 'Linux':
    PATH_OF_GIT_REPO = os.getcwd() + '/.git'  # Pastas .git do repositório no Linux
    print(f'Pasta .git no {my_os}: {PATH_OF_GIT_REPO}')
else:
    print(f'Sistema Operacional {my_os} não identificado.')
    exit()

# Auto push no Github
COMMIT_MESSAGE = f'PI4: Auto update em: {conteudo.intervalo / 60:.2f} minutos'


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


# Baixando o arquivos .csv
def baixar_csv():
    response = requests.get(fontedados.url_acoes)
    open("resultado/dadosacoes.csv", "wb").write(response.content)
    response = requests.get(fontedados.url_fiis)
    open("resultado/dadosfiis.csv", "wb").write(response.content)


# Lendo e salvando os arquivos .csv
def ler_csv():
    pd.read_csv(r'resultado/dadosacoes.csv', sep=";", decimal='.')
    pd.read_csv(r'resultado/dadosfiis.csv', sep=";", decimal='.')


# Atualizador em loop
def atualizar():
    baixar_csv()
    ler_csv()
    conteudo.lastupdate()
    conteudo.criar_readme()
    git_push()
    print('Auto update: OK.')
    print(f'Atualização a cada {conteudo.intervalo / 60:.2f} minutos')
    print(f'Última atualização: {conteudo.last_update}.')


schedule(atualizar, interval=conteudo.intervalo)
run_loop()
