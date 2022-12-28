import requests
import pandas as pd

# Acoes
def acoes2():
    url = "https://statusinvest.com.br/category/advancedsearchresult"

    querystring = {
        "search": "{\"Sector\":\"\",\"SubSector\":\"\",\"Segment\":\"\",\"my_range\":\"-20;100\",\"forecast\":{\"upsideDownside\":{\"Item1\":null,\"Item2\":null},\"estimatesNumber\":{\"Item1\":null,\"Item2\":null},\"revisedUp\":true,\"revisedDown\":true,\"consensus\":[]},\"dy\":{\"Item1\":null,\"Item2\":null},\"p_L\":{\"Item1\":null,\"Item2\":null},\"peg_Ratio\":{\"Item1\":null,\"Item2\":null},\"p_VP\":{\"Item1\":null,\"Item2\":null},\"p_Ativo\":{\"Item1\":null,\"Item2\":null},\"margemBruta\":{\"Item1\":null,\"Item2\":null},\"margemEbit\":{\"Item1\":null,\"Item2\":null},\"margemLiquida\":{\"Item1\":null,\"Item2\":null},\"p_Ebit\":{\"Item1\":null,\"Item2\":null},\"eV_Ebit\":{\"Item1\":null,\"Item2\":null},\"dividaLiquidaEbit\":{\"Item1\":null,\"Item2\":null},\"dividaliquidaPatrimonioLiquido\":{\"Item1\":null,\"Item2\":null},\"p_SR\":{\"Item1\":null,\"Item2\":null},\"p_CapitalGiro\":{\"Item1\":null,\"Item2\":null},\"p_AtivoCirculante\":{\"Item1\":null,\"Item2\":null},\"roe\":{\"Item1\":null,\"Item2\":null},\"roic\":{\"Item1\":null,\"Item2\":null},\"roa\":{\"Item1\":null,\"Item2\":null},\"liquidezCorrente\":{\"Item1\":null,\"Item2\":null},\"pl_Ativo\":{\"Item1\":null,\"Item2\":null},\"passivo_Ativo\":{\"Item1\":null,\"Item2\":null},\"giroAtivos\":{\"Item1\":null,\"Item2\":null},\"receitas_Cagr5\":{\"Item1\":null,\"Item2\":null},\"lucros_Cagr5\":{\"Item1\":null,\"Item2\":null},\"liquidezMediaDiaria\":{\"Item1\":null,\"Item2\":null},\"vpa\":{\"Item1\":null,\"Item2\":null},\"lpa\":{\"Item1\":null,\"Item2\":null},\"valorMercado\":{\"Item1\":null,\"Item2\":null}}",
        "CategoryType": "1"}

    payload = ""
    headers = {
        "authority": "statusinvest.com.br",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "dnt": "1",
        "referer": "https://statusinvest.com.br/acoes/busca-avancada",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.text)

    json_res = response.json()

    res = []

    for i in json_res:
        res.append(i)

    df = pd.json_normalize(res)
    df = pd.DataFrame(df)
    df.to_csv('acoes2.csv', encoding='utf-8', index=False, sep=';', decimal=',')


# FII's
def fiis2():
    url = "https://statusinvest.com.br/category/advancedsearchresult"

    querystring = {
        "search": "{\"Segment\":\"\",\"Gestao\":\"\",\"my_range\":\"0;20\",\"dy\":{\"Item1\":null,\"Item2\":null},\"p_vp\":{\"Item1\":null,\"Item2\":null},\"percentualcaixa\":{\"Item1\":null,\"Item2\":null},\"numerocotistas\":{\"Item1\":null,\"Item2\":null},\"dividend_cagr\":{\"Item1\":null,\"Item2\":null},\"cota_cagr\":{\"Item1\":null,\"Item2\":null},\"liquidezmediadiaria\":{\"Item1\":null,\"Item2\":null},\"patrimonio\":{\"Item1\":null,\"Item2\":null},\"valorpatrimonialcota\":{\"Item1\":null,\"Item2\":null},\"numerocotas\":{\"Item1\":null,\"Item2\":null},\"lastdividend\":{\"Item1\":null,\"Item2\":null}}",
        "CategoryType": "2"}

    payload = ""
    headers = {
        "authority": "statusinvest.com.br",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "dnt": "1",
        "referer": "https://statusinvest.com.br/fundos-imobiliarios/busca-avancada",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    json_res = response.json()

    res = []

    for i in json_res:
        res.append(i)

    df = pd.json_normalize(res)
    df = pd.DataFrame(df)
    df.to_csv('fiis2.csv', encoding='utf-8', index=False, sep=';', decimal=',')



acoes2()
fiis2()


