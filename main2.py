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
intervalo = 10  # 14400s = 4h / 7200s = 2h
agora = datetime.datetime.now()
last_update = agora.strftime("%d-%m-%Y ás %H:%M:%S")

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
COMMIT_MESSAGE = f'PI4: Auto update em: {intervalo / 60:.2f} minutos'


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


def criar_readme():
    #
    readme_conteudo = f"""
    # StatusInvest - Dados
    Informações das Ações e dos FII's listados na StatusInvest atualizadas a cada {intervalo / 60:.2f} minutos rodando em um [Raspberry Pi 4 Model B](https://www.raspberrypi.com/) que estava parado.

    Atualização automática em: {intervalo / 60:.2f} minutos. <br>
    <br>Última atualização: {last_update}.  <br>


    >Resultados: <br>
    [Ações - Googlesheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vS97G13-9owVwSm1y_TAE3gTaxYflhMvgXCYgj3zEGVwqrbPiUrsOyUUcdhM5D7YVJPNaiinn51Plgc/pubhtml?gid=313887204&single=true) <br>
    [Ações - .csv](https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/resultado/dadosacoes.csv) <br>
    [FII's - Googlesheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vS97G13-9owVwSm1y_TAE3gTaxYflhMvgXCYgj3zEGVwqrbPiUrsOyUUcdhM5D7YVJPNaiinn51Plgc/pubhtml?gid=1741348998&single=true) <br>
    [FII's - .csv](https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/resultado/dadosfiis.csv) <br>


    Exemplo de uso no Googlesheets:
    ```sh
    =IMPORTDATA("https://raw.githubusercontent.com/Antxj/StatusInvestDados/master/resultado/dadosacoes.csv";";";"pt_BR")
    ```

    ![img_2.png](exemplo.png)

    """
    #
    leitor = open("README.md", "w")  # encoding="cp1252" testar
    leitor.write(readme_conteudo)
    leitor.close()
    print('Readme.md: OK.')


def atualizar():
    # Baixando o arquivos .csv
    response = requests.get(fontedados.url_acoes)
    open("resultado/dadosacoes.csv", "wb").write(response.content)
    response = requests.get(fontedados.url_fiis)
    open("resultado/dadosfiis.csv", "wb").write(response.content)

    # Lendo e salvando os arquivos .csv
    pd.read_csv(r'resultado/dadosacoes.csv', sep=";", decimal='.')
    pd.read_csv(r'resultado/dadosfiis.csv', sep=";", decimal='.')

    # Quando executou
    agora = datetime.datetime.now()
    last_update = agora.strftime("%d-%m-%Y ás %H:%M:%S")

    # Readme.md
    criar_readme()

    # Push
    git_push()
    print('Auto update: OK.')
    print(f'Atualização a cada {intervalo / 60:.2f} minutos')
    print(f'Última atualização: {last_update}.')




schedule(atualizar, interval=intervalo)
run_loop()
