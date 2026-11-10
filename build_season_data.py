import glob
from io import StringIO
import pandas as pd

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

def read_nasa(path):
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("PARAMETER,"))
    df = pd.read_csv(StringIO("\n".join(lines[start:])))
    return df.replace(-999, float("nan"))

# 1. Weather: average of all locations
frames = []
for path in sorted(glob.glob("data/weather/weather_*.csv")):
    d = read_nasa(path).melt(id_vars=["PARAMETER", "YEAR"], value_vars=MONTHS,
                             var_name="MON", value_name="value")
    d["month"] = d["MON"].map({m: i + 1 for i, m in enumerate(MONTHS)})
    frames.append(d)
print("Weather files:", len(frames))
w = pd.concat(frames).groupby(["PARAMETER", "YEAR", "month"], as_index=False)["value"].mean()

rain = w[(w.PARAMETER == "PRECTOTCORR") & w.month.between(6, 9)]
temp = w[(w.PARAMETER == "T2M") & w.month.between(6, 9)]
wy = pd.DataFrame({
    "start_year": rain.groupby("YEAR")["value"].mean().index,
    "rain_jun_sep": rain.groupby("YEAR")["value"].mean().values,
    "temp_jun_sep": temp.groupby("YEAR")["value"].mean().values,
})

# 2. Yield
y = pd.read_csv("data/yield/cotton_yield_long.csv")
y["start_year"] = y["season"].str[:4].astype(int)

out = y.merge(wy, on="start_year", how="left").round(2)
out.to_csv("data/processed/season_data.csv", index=False)
print(out.to_string(index=False))
print("\nTotal seasons:", len(out), "| complete:", len(out.dropna()))