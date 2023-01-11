
#%%
import json
import requests


# %%
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
retorno = requests.get(url)


#%%
if retorno:
    print(retorno.text)
else: 
    print('Falhou!!')


# %%
cotacao_json = json.loads(retorno.text)['USDBRL']
print(f"1 dolár custam hoje {cotacao_json['bid']}")


# %%
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    retorno = requests.get(url)
    cotacao_json = json.loads(retorno.text)[moeda.replace('-', '')]
    print(f"{valor} {moeda[:3]} hoje custam {round(float(cotacao_json['bid']) * valor, 3)} {moeda[-3:]}")

cotacao(10, 'USD-BRL')

cotacao(10, 'JPY-BRL')

#%%
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


# %%
log
formatter
ch
# %%
