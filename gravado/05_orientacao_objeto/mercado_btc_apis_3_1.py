from abc import ABC, abstractmethod
import datetime
import logging

from backoff import expo, on_exception
import ratelimit
import requests

logger = logging.getLogger(__name__) 
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinAPI(ABC):
    
    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
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

    def get_unix_epochs(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    
    def _get_endpoint(self,
                      date_from: datetime.date = None,
                      date_to: datetime.date = None) -> str:

        if date_from and not date_to:          
            unix_date_from = self.get_unix_epochs(date_from)
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}'

        elif date_from and date_to:
            if date_from > date_to:
                raise RuntimeError("date_from cannot be greater than date_to")
            unix_date_from = self.get_unix_epochs(date_from)
            unix_date_to = self.get_unix_epochs(date_to)
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}'

        else: # Retorna as últimas mil transações
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}'

        return endpoint