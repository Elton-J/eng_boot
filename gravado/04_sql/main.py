# %%
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

# %%
engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db')
engine

# %%

query = """select *

         from ingredients"""

df = pd.read_sql(query, engine)
df

# %%
