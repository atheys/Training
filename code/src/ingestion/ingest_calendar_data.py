"""module for ingesting calendar data"""

# module imports

from datetime import datetime, timedelta
from code.utils.engines import dwh_engine

# library imports
import pandas as pd

today = datetime.today()
start = datetime(1990, 1, 1)
end = datetime(today.year + 5, 12, 31)

calendar = []
for i in range((end - start).days + 1):
  date = start + timedelta(days=i)
  temp = {
    "datetime": date,
    "date": date.date(),
    "year": date.year,
    "year_label": date.strftime("%y"),
    "month": date.month,
    "month_label": date.strftime("%b"),
    "month_label_long": date.strftime("%B"),
    "day": date.day,
    "iso_year": date.year,
    "iso_week": int(date.strftime("%W")),
    "iso_day": 7 if int(date.strftime("%w")) == 0 else int(date.strftime("%w")),
    "iso_day_label": date.strftime("%a"),
    "iso_day_label_long": date.strftime("%A")
  }
  temp["this_year"] = int(temp["year"] == today.year)
  temp["this_year_label"] = "Yes" if bool(temp["this_year"]) else "No"
  temp["this_year_label_order"] = int(not temp["this_year"])
  temp["last_year"] = int(temp["year"] == (today.year - 1))
  temp["last_year_label"] = "Yes" if bool(temp["last_year"]) else "No"
  temp["last_year_label_order"] = int(not temp["last_year"])
  temp["this_month"] = int(temp["month"] == today.month)
  temp["this_month_label"] = "Yes" if bool(temp["this_month"]) else "No"
  temp["this_month_label_order"] = int(not temp["this_month"])
  temp["last_month"] = int(temp["month"] == (today.month - 1) or \
                           (temp["month"] == 12 and today.month == 1))
  temp["last_month_label"] = "Yes" if bool(temp["last_month"]) else "No"
  temp["last_month_label_order"] = int(not temp["last_month"])
  temp["this_day"] = int(temp["day"] == today.day)
  temp["this_day_label"] = "Yes" if bool(temp["this_day"]) else "No"
  temp["this_day_label_order"] = int(not temp["this_day"])
  temp["this_iso_year"] = temp["this_year"]
  temp["this_iso_year_label"] = temp["this_year_label"]
  temp["this_iso_year_label_order"] = int(not temp["this_iso_year"])
  temp["last_iso_year"] = temp["last_year"]
  temp["last_iso_year_label"] = temp["last_year_label"]
  temp["last_iso_year_label_order"] = int(not temp["last_iso_year"])
  temp["this_iso_week"] = int(temp["iso_week"] == int(today.strftime("%W")))
  temp["this_iso_week_label"] = "Yes" if bool(temp["this_iso_week"]) else "No"
  temp["this_iso_week_label_order"] = int(not temp["this_iso_week"])
  temp["last_iso_week"] = int(temp["iso_week"] == (int(today.strftime("%W")) - 1) or \
                              (temp["iso_week"] >= 52 and int(today.strftime("%W")) == 1))
  temp["last_iso_week_label"] = "Yes" if bool(temp["last_iso_week"]) else "No"
  temp["last_iso_week_label"] = int(not temp["last_iso_week"])
  t = 7 if int(today.strftime("%w")) == 0 else int(today.strftime("%w"))
  temp["this_iso_day"] = int(temp["iso_day"] == t)
  temp["this_iso_day_label"] = "Yes" if bool(temp["this_iso_day"]) else "No"
  temp["this_iso_day_label_order"] = int(not temp["this_iso_day"])
  temp["last_iso_day"] = int(temp["iso_day"] == (t-1) or \
                             (temp["iso_day"] == 7 and t == 1) )
  temp["last_iso_day_label"] = "Yes" if bool(temp["last_iso_day"]) else "No"
  temp["last_iso_day_label_order"] = int(not temp["last_iso_day"])
  temp["year_to_date"] = int(temp["month"] < today.month or (temp["month"] == today.month and temp["day"] <= today.day))
  temp["year_to_date_label"] = "Yes" if bool(temp["year_to_date"]) else "No"
  temp["year_to_date_label"] = int(not temp["year_to_date"])
  temp["month_to_date"] = int(temp["day"] <= today.day)
  temp["month_to_date_label"] = "Yes" if bool(temp["month_to_date"]) else "No"
  temp["month_to_date_label_order"] = int(not temp["month_to_date"])
  temp["iso_week_to_date"] = int(temp["iso_day"] <= t)
  temp["iso_week_to_date_label"] = "Yes" if bool(temp["iso_week_to_date"]) else "No"
  temp["iso_week_to_date_label_order"] = int(not bool(temp["iso_week_to_date"]))
  temp["month_count"] = int(100 * temp["year"] + temp["month"])
  temp["iso_week_count"] = int(100 * temp["year"] + temp["iso_week"])
  temp["iso_day_count"] = int(10 * temp["iso_week"] + temp["iso_day"])
  temp["month_max"] = 12 + temp["month"] if temp["month"] <= today.month else temp["month"]
  temp["iso_week_max"] = 53 + temp["iso_week"] if temp["iso_week"] <= int(today.strftime("%W")) else temp["iso_week"]
  calendar.append(temp)

df = pd.DataFrame.from_dict(calendar)
df.to_sql("calendar_jay_z", dwh_engine, index=False, if_exists="replace")
df.to_parquet("calendar.parquet", index=False)
