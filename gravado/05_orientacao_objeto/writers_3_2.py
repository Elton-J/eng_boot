

import datetime
import json
import os
from typing import List


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
