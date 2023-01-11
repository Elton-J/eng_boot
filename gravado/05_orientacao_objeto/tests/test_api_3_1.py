
import datetime
import pytest
from mercado_btc_apis_3_1 import DaySummaryAPI
from mercado_btc_apis_3_1 import TradesAPI


class TestDaySummaryApi:

    @pytest.mark.parametrize(

                "coin, date, expected",

                [
                    ('BTC', datetime.date(2021, 4, 1), 'https://www.mercadobitcoin.net/api/BTC/day-summary/2021/4/1'),
                    ('ETH', datetime.date(2021, 9, 7),  'https://www.mercadobitcoin.net/api/ETH/day-summary/2021/9/7'),
                    ('BTC', datetime.date(2022, 8, 1), 'https://www.mercadobitcoin.net/api/BTC/day-summary/2022/8/1'),
                    
                ]

    )

    def teste_get_endpoint(self, coin, date, expected):
        api = DaySummaryAPI(coin=coin)
        actual = api._get_endpoint(date=date)
        expected = expected

        assert actual == expected



class TestTradesApi:
    
    @pytest.mark.parametrize(

                "coin, date_from, date_to, expected",

                [
                    ('TEST', datetime.datetime(2018, 12, 1), datetime.datetime(2019, 1, 1),
                     'https://www.mercadobitcoin.net/api/TEST/trades/1543629600/1546308000'),
                    ('TEST', None, None, 
                    'https://www.mercadobitcoin.net/api/TEST/trades'),
                    ('TEST', None, datetime.datetime(2019, 1, 1), 
                    'https://www.mercadobitcoin.net/api/TEST/trades'),
                    ('TEST', datetime.datetime(2018, 12, 1), None,
                     'https://www.mercadobitcoin.net/api/TEST/trades/1543629600')
                ]

    )

    def test_get_endpoint(self, coin, date_from, date_to, expected):
        api = TradesAPI(coin=coin)
        actual = api._get_endpoint(date_from=date_from, date_to=date_to)
        expected = expected

        assert actual == expected

    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):

            TradesAPI(coin='TEST')._get_endpoint(date_from=datetime.datetime(2022, 1, 1),
                                                date_to=datetime.datetime(2005, 1, 1))


    @pytest.mark.parametrize(

                "date, expected",

                [
                    (datetime.datetime(2019, 1, 1), 1546308000),
                    (datetime.datetime(2018, 12, 1), 1543629600),
                    (datetime.datetime(1999, 5, 1, 0, 0, 5), 925527605),
                ]

    )

    def test_get_unix_epoch(self, date, expected):
        actual = TradesAPI(coin='TEST').get_unix_epochs(date=date)
        assert actual == expected