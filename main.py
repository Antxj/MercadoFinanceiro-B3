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

readme_conteudo = f"""
# StatusInvest - Dados
Informações das Ações e dos FII's listados na StatusInvest atualizadas a cada x minutos rodando em um [Raspberry Pi 4 Model B](https://www.raspberrypi.com/) que estava parado.

Atualização automática em: {intervalo/60:.2f} minutos. <br>
Última atualização: {last_update}


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
COMMIT_MESSAGE = f'PI4: Auto update {intervalo / 60:.2f} minutos'


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
    leitor = open("README.md", "w", encoding="cp1252")
    leitor.write(readme_conteudo)
    print("Readme.md: OK.")


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

    # Push
    criar_readme()
    time.sleep(5)
    git_push()

    print(f'Atualização a cada {intervalo / 60:.2f} minutos')
    print(f'Última atualização: {last_update}.')


schedule(atualizar, interval=intervalo)
run_loop()


