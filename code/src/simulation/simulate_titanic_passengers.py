"""module for simulating passenger details"""

# module imports
from datetime import datetime, timedelta
from code.utils.engines import dwh_engine

# library imports
import json
import random
import numpy as np
import pandas as pd


df = pd.read_sql_table("titanic", dwh_engine)
records = json.loads(df.to_json(orient= "records"))

data = []
inches = 0.0254
bmi = 22.5
male = [38.8, 47.5, 53.9, 60.9, 68.3, 69.6, 69.9]
female = [35., 44., 50., 55.5, 62.75, 66.75, 68.25]
male = [m * inches for m in male]
female = [f * inches for f in female]
for i in range(len(records)):
    age = records[i]["age"]
    birthdate = None
    if age:
        end_date = datetime(1912 - int(age), 4, 15)
        start_date = datetime(1912 - int(age) - 1, 4, 15)
        birthdate = datetime.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))
    temp = {
        "id": records[i]["id"],
        "birthdate": birthdate
    }
    a = min(max(int(round(records[i]["age"] / 3.)) - 1, 0), 6) if records[i]["age"] else 6
    gender = records[i]["gender"]
    if gender == "male":
        mu = male[a]
        sigma = 1.5 * inches
        h = np.random.normal(mu, sigma, 1)[0]
    else:
        mu = female[a]
        sigma = 1.5 * inches
        h = np.random.normal(mu, sigma, 1)[0]

    mu_w = mu * mu * bmi
    sigma_w = 0.85 * max(a, 1) * 3
    w = np.random.normal(mu_w, sigma_w, 1)[0]
    temp["height"] = round(h, 3)
    temp["weight"] = round(w, 2)
    temp["bmi"] = w / (h*h)
    data.append(temp)

df = pd.DataFrame.from_dict(data)
df.to_sql("titanic_passengers", dwh_engine, index=False, if_exists="replace")
df.to_csv("../../../data/csv/titanic_passengers.csv", index=False, sep=";", decimal=",")
