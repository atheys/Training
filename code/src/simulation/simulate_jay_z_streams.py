"""module for simulating passenger details"""

# module imports
from datetime import datetime, timedelta
from code.utils.engines import dwh_engine

# library imports
import json
import random
import numpy as np
import pandas as pd


df = pd.read_sql_table("jay_z", dwh_engine)
records = json.loads(df.to_json(orient= "records"))

records = [(
    r["album_title"],
    r["song"],
    datetime.utcfromtimestamp(r["date"] / 1000.).year,
    r["track"]
) for r in records]
records = list(set(records))

data = []
for i in range(len(records)):
    base = {
        "album_title": records[i][0],
        "song": records[i][1]
    }
    y = records[i][2]
    t = records[i][3]
    start = 2006
    end = datetime.today().year
    for i in range(max(start, y), datetime.today().year + 1):
        temp = dict(base)
        revenue = 0.003 + 0.002 * ((i - start) / (end - start))
        500000000.* random.random() * 0.9 ** (i-y)
        temp["year"] = i
        temp["streams"] = int(75000000. * random.random() * 0.9 ** (i-y) * (20 - t) / 20.)
        temp["revenue_per_stream"] = round(revenue, 5)
        data.append(temp)

df = pd.DataFrame.from_dict(data)
df.to_sql("jay_z_streams", dwh_engine, index=False, if_exists="replace")

