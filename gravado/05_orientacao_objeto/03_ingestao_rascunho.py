#%%
import datetime
import json
import os
import time
from typing import List
import requests
import logging
from abc import ABC, abstractmethod
import schedule
#%%
## TESTE API
#moeda = 'BTC'
#url = f'https://www.mercadobitcoin.net/api/{moeda}/day-summary/2023/1/3/'

#btc = requests.get(url).json()
#btc

# %%
logger = logging.getLogger(__name__) # main se rodar local, ou nome do script: ingestao, se for importado
logging.basicConfig(level=logging.INFO)

# %%
class MercadoBitcoinAPI(ABC): # Classe abstrata (abstract basic class)
    
    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f'Obtendo dados do endpoint: {endpoint}')
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()


class DaySummaryAPI(MercadoBitcoinAPI):
    
    type = 'day-summary'
    
    def _get_endpoint(self, date: datetime.date) -> str:
        return f'{self.base_endpoint}/{self.coin}/{self.type}' \
               f'/{date.year}/{date.month}/{date.day}'

class TradesAPI(MercadoBitcoinAPI):

    type = 'trades'

    def get_unix_epochs(self, date: datetime) -> int:
        return int(date.timestamp())

    
    def _get_endpoint(self,
                      date_from: datetime.date = None,
                      date_to: datetime.date = None) -> str:

        if date_from and not date_to:
            
            unix_date_from = self.get_unix_epochs(date_from)
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}'

        elif date_from and date_to:
            
            unix_date_from = self.get_unix_epochs(date_from)
            unix_date_to = self.get_unix_epochs(date_to)
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}'

        else: # Retorna as últimas mil transações
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}'

        return endpoint

class DataTypeNotSupportedForIngestionException(Exception):
    
    def __init__(self, data):
        self.data = data
        self.message = f'Data type {type(data)} is not supported for ingestion'
        super().__init__(self.message) # Joga esse argumento pra classe mãe.


class DataWriter:

    def __init__(self, api: str, coin = str) -> None:
        self.api = api
        self.coin = coin
        self.filename = f'{self.api}/{self.coin}/{datetime.datetime.now()}.json'

    def _write_row(self, row: str) -> None:

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, mode='a') as f: # Append
            f.write(row)

    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + '\n')

        elif isinstance(data, List):
            for element in data:
                self.write(element) # Recursiva

        else:
            raise DataTypeNotSupportedForIngestionException(data)


class DataIngestor(ABC):
    
    def __init__(self, writer: DataWriter, coins: List[str], default_start_date: datetime.datetime) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = None

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            self._checkpoint

    def _update_checkpoint(self, value):
        self._checkpoint = value


    @abstractmethod
    def ingest(self) -> None:
        pass

class DaySummaryIngestor(DataIngestor):

    def __init__(self, writer: DataWriter, coins: List[str], default_start_date: datetime.datetime) -> None:
        super().__init__(writer, coins, default_start_date)
        self.writer = DataWriter

    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryAPI(coin=coin)
                data = api.get_data(date=date)
                self.writer(api=api.type, coin=coin).write(data)

            self._update_checkpoint(date + datetime.timedelta(days=1))


ingestor_daysummary = DaySummaryIngestor(writer=writer, coins=['BTC', 'ETH', 'LTC'],
                                         default_start_date=datetime.date(2023, 1, 1))

@schedule.repeat(schedule.every(1).seconds)
def job():
    ingestor_daysummary.ingest()

while True:
    schedule.run_pending()
    time.sleep(1)








# %%
print(DaySummaryAPI(coin='BTC').get_data(date=datetime.date(2022, 1, 3)))
# %%
print(TradesAPI(coin='BTC').get_data())

# %%
print(TradesAPI(coin='BTC').get_data(date_from = datetime.datetime(2023, 1, 1)))
# %%
print(TradesAPI(coin='BTC').get_data(date_from = datetime.datetime(2023, 1, 1),
                                     date_to = datetime.datetime(2023, 1, 3))                          )

# %%
# TESTA DATA WRITER DAY SUMMARY
day_summary = DaySummaryAPI(coin='BTC').get_data(date=datetime.date(2023, 1, 3))
day_summary
# %%

writer = DataWriter(filename='day_summary_20230103.json')
writer.write(day_summary)

# %%
# TESTA DATA WRITER TRADES
trades = TradesAPI(coin='BTC').get_data(date_from = datetime.datetime(2023, 1, 1),
                                        date_to = datetime.datetime(2023, 1, 3))
trades
# %%

writer = DataWriter(filename='trades_20230101_20230103.json')
writer.write(trades)

# Erro por tipo
writer.write(4)

# %%
# TESTE INGESTAO DAY SUMMARY
writer = DataWriter(filename='day_summary_ingestor.json')

ingestor_daysummary = DaySummaryIngestor(writer=writer, coins=['BTC', 'ETH', 'LTC'],
                                         default_start_date=datetime.date(2023, 1, 1))

ingestor_daysummary.ingest()


# %%
ingestor_new = DaySummaryIngestor(writer=writer, coins=['BTC', 'ETH', 'LTC'],
                                  default_start_date=datetime.date(2023, 1, 1))

ingestor_new.ingest()
# %%
