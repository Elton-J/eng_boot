
import datetime

from writers_3_2 import DataWriter
from ingestors_3_3 import DaySummaryIngestor

from schedule import repeat, every, run_pending

import time


if __name__ == 'main':

    ingestor_daysummary = DaySummaryIngestor(
                            writer=DataWriter,
                            coins=['BTC', 'ETH', 'LTC'],
                            default_start_date=datetime.date(2022, 11, 1)
                            )

    @repeat(every(1).seconds)
    def job():
        ingestor_daysummary.ingest()

    while True:
        run_pending()
        time.sleep(1)







# %%
