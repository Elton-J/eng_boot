#%% 
import logging
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://portalcafebrasil.com.br/todos/podcasts/'

retorno = requests.get(url)

retorno.text


# %%
soup = bs(retorno.text)
soup

# %%
lista_podcasts = soup.find_all('h5')
lista_podcasts

# %%
# Só vem os que aparecem na página
for pod in lista_podcasts:
    print(f"EP: {pod.text}  \n Link: {pod.a['href']}")


# %%
url_network = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

def get_podcast(url, pagina):
    retorno = requests.get(url.format(pagina))
    retorno.text
    soup = bs(retorno.text)
    return soup.find_all('h5')

get_podcast(url_network, pagina=10)

#%%
# Log
log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)



# %%
pag = 1
lista_podcasts = []
lista_pag_temp = get_podcast(url_network, pagina=pag)


log.debug(f"Coletados {len(lista_pag_temp)} episódios do link {url_network.format(pag)}")

while len(lista_pag_temp) > 0:
    lista_podcasts = lista_podcasts + lista_pag_temp
    pag += 1
    lista_pag_temp = get_podcast(url_network, pagina=pag)
    log.debug(f"Coletados {len(lista_pag_temp)} episódios do link {url_network.format(pag)}")



# %%
lista_podcasts

# %%
df = pd.DataFrame(columns=['nome', 'link'])
df

# %%
for item in lista_podcasts:
    df.loc[df.shape[0]] = [item.text, item.a['href']]

df

# %%
