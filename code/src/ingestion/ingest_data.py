"""module for ingesting data into DWH"""

# module imports
from code.utils.engines import dwh_engine

# library imports
import re
import pandas as pd

# data set Jay Z
df_jay_z = pd.read_csv("/Users/andreastheys/Documents/Projects/Training/data/ingestion/jay_z.csv", sep=";", encoding="latin-1")
df_jay_z["date"] = pd.to_datetime(df_jay_z["date"], format="%m/%d/%Y", errors="ignore")
df_jay_z.to_sql("jay_z", dwh_engine, index=False, if_exists="replace")

# data set Titanic
df_titanic = pd.read_csv("/Users/andreastheys/Documents/Projects/Training/data/ingestion/titanic.csv", sep=";", encoding="latin-1")

formatted_names = list(df_titanic["name"])
titles = ["Mr.", "Mrs.", "Miss.", "Ms."]
for i in range(len(formatted_names)):
    temp = formatted_names[i].split(", ")
    for title in titles:
        temp[1] = temp[1].replace(title, "")
    formatted_names[i] = temp[1].strip() + " " + temp[0].strip()
    formatted_names[i] = re.sub("[\(\[].*?[\)\]]", "", formatted_names[i])
    formatted_names[i] = formatted_names[i].replace("  ", " ").strip()
df_titanic["name"] = formatted_names

formatted_fares = list(df_titanic["fare"])
for i in range(len(formatted_fares)):
    N = formatted_fares[i].count(".")
    if N > 1:
        formatted_fares[i] = formatted_fares[i].replace(".", "", N - 1)
    formatted_fares[i] = round(float(formatted_fares[i]), 2)
df_titanic["fare"] = formatted_fares
df_titanic.to_sql("titanic", dwh_engine, index=False, if_exists="replace")
