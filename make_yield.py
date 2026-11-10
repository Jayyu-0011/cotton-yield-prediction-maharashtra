import pandas as pd

# Maharashtra cotton (lint) yield, Kg per Hectare
# Source: RBI Handbook of Statistics on Indian States, Table 86
seasons = ["2004-05", "2005-06", "2006-07", "2007-08", "2008-09", "2009-10",
           "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16",
           "2016-17", "2017-18", "2018-19", "2019-20", "2020-21", "2021-22",
           "2022-23", "2023-24", "2024-25"]
yields = [176, 187, 253, 373, 257, 285, 367, 297, 314, 358, 284, 303,
          475, 238, 266, 251, 378, 318, 338, 323, 304]

df = pd.DataFrame({"season": seasons, "yield_kg_per_ha": yields})
df.to_csv("data/yield/cotton_yield_long.csv", index=False)
print(df.to_string(index=False))
print("Total seasons:", len(df))