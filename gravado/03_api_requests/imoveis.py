# %%

# Bibliotecas
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# %%
url = 'https://www.vivareal.com.br/venda/sp/santo-andre/apartamento_residencial/'



pag = 1
retorno = requests.get(url.format(pag))
soup = bs(retorno.text)

# %%
# De acordo com o inspect (F12) do site, essa classe contem as informações
# de cada card (imóvel)

casas = soup.find_all('a', {'class': 'property-card__labels-container js-main-info js-listing-labels-link'})

# Classe com o total de imóveis
qtd_casas = soup.find_all('strong', {'class': 'results-summary__count js-total-records'})
qtd_casas[0].text#.replace('.', '')


# %%
casa = casas[0]
casa

# %%

# %%
