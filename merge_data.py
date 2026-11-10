import glob
from io import StringIO
import pandas as pd

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

def read_nasa(path):
    # NASA files have header text first, then the real table
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("PARAMETER,"))
    df = pd.read_csv(StringIO("\n".join(lines[start:])))
    return df.replace(-999, float("nan"))   # -999 means no data

# ---- 1. Weather: average of all locations ----
frames = []
for path in sorted(glob.glob("data/weather/weather_*.csv")):
    d = read_nasa(path).melt(id_vars=["PARAMETER", "YEAR"], value_vars=MONTHS,
                             var_name="MON", value_name="value")
    d["month"] = d["MON"].map({m: i + 1 for i, m in enumerate(MONTHS)})
    frames.append(d)
print("Weather files:", len(frames))

w = pd.concat(frames).groupby(["PARAMETER", "YEAR", "month"], as_index=False)["value"].mean()
rain = w[w.PARAMETER == "PRECTOTCORR"]
temp = w[w.PARAMETER == "T2M"].set_index(["YEAR", "month"])["value"]
monsoon = rain[rain.month.between(6, 9)].groupby("YEAR")["value"].mean()

# ---- 2. Price ----
p = pd.read_csv("data/processed/maharashtra_price.csv", parse_dates=["date"])
p["month"] = p["date"].dt.month
start = p["date"].dt.year.where(p["month"] >= 10, p["date"].dt.year - 1)
p["season"] = start.astype(str) + "-" + (start + 1).astype(str).str[-2:]
p["rain_jun_sep"] = start.map(monsoon).round(2)
p["temp_month"] = [temp.get((y, m)) for y, m in zip(p["date"].dt.year, p["month"])]
p["temp_month"] = p["temp_month"].round(2)

# ---- 3. Yield ----
y = pd.read_csv("data/yield/cotton_yield.csv")
out = p.merge(y, on="season", how="left")
out = out[["date", "season", "avg_modal_price", "arrivals_tonnes",
           "rain_jun_sep", "temp_month", "yield_kg_per_ha"]]
out.to_csv("data/processed/merged.csv", index=False)

print(out.to_string(index=False))
print("\nTotal rows:", len(out))
print("Complete rows (no missing values):", len(out.dropna()))