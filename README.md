# Cotton Yield Prediction & Price Trend Analysis (Maharashtra)

A beginner-friendly data science project that studies how monsoon rain relates to
cotton yield in Maharashtra, and looks at how cotton prices behaved over time.

## What this project does
1. Collects real data: market prices, state yield, and weather.
2. Cleans and joins it into one table (one row per cotton season).
3. Builds a simple model (Linear Regression) that estimates yield from monsoon rain.
4. Tests the model honestly with Leave-One-Out validation.
5. Shows price trends with charts and compares them with world cotton prices
   (world price file: `data/processed/world_cotton_price_monthly.csv`).

## Data sources
| Data | Source | Coverage |
|---|---|---|
| Market prices | Agmarknet, commodity-wise daily reports | 30 report dates (Oct-Dec, 2021-2026), Maharashtra weighted average |
| Cotton yield (kg/ha, lint) | RBI Handbook of Statistics on Indian States, Table 86 | 21 seasons, 2004-05 to 2024-25 |
| Weather (rain, temperature) | NASA POWER, monthly | Jalgaon, Akola, Yavatmal, 2004-2025 |
| World cotton price (Cotton A Index, US$/kg) | World Bank Commodity Markets (Pink Sheet), monthly historical file | Monthly, 2004-2026 (used for the price comparison in the notebook) |

## Method
- Weather is averaged over three cotton-belt locations (Jalgaon, Akola, Yavatmal).
- Feature used: average daily rain from June to September (`rain_jun_sep`).
- Target: state cotton yield (kg per hectare) for the season.
- Model: Linear Regression, checked with Leave-One-Out cross-validation
  (hide one season, predict it from the other 20, repeat for all 21).

## Results
| Predictor | Average error (kg/ha) |
|---|---|
| Always guess the average (baseline) | 52.7 |
| Monsoon rain only | **49.0** |
| Rain + temperature | 51.3 |

- Correlation of monsoon rain with yield: +0.38 (mild).
- Rule of thumb from the model: +1 mm/day of monsoon rain is about +22 kg/ha yield.
- Example estimates (typical error about +/- 49 kg/ha):
  dry year (rain 5.0) about 263, normal (6.8) about 302, wet (8.5) about 339 kg/ha.

## Limitations (please read)
- Only 21 seasons of yield data, so the model is only slightly better than guessing the average.
- Yield depends on many things not in this data (pests, seed type, irrigation, area).
- Price data covers only 30 dates (Oct-Dec), so **no price model was built**; prices are
  analysed with charts only. World cotton price vs Indian price correlation is +0.57 on
  well-supplied dates, but it did not predict well when a whole year was held out.
- Weather is an average of three locations, not district-level.

## Future work
- Get a long monthly history of Indian cotton prices (for example the WPI "Raw Cotton"
  index from the Office of the Economic Adviser) and build a price model.
- Use district-wise yield and weather, and add area, irrigation and pest data.

## Project structure
```
data/
  raw/        daily Agmarknet report files
  processed/  maharashtra_price.csv, season_data.csv, world_cotton_price_monthly.csv
  yield/      cotton_yield_long.csv
  weather/    weather_jalgaon.csv, weather_akola.csv, weather_yavatmal.csv
notebooks/    01_cotton_analysis.ipynb (charts, model, predictions)
combine_prices.py     builds Maharashtra price table from daily reports
make_yield.py         writes the yield table (RBI Table 86)
build_season_data.py  joins yield + weather into season_data.csv
```

## How to run
```
pip install pandas matplotlib scikit-learn jupyter ipykernel
python combine_prices.py
python make_yield.py
python build_season_data.py
```
Then open `notebooks/01_cotton_analysis.ipynb` and run all cells.

## Author
Jayesh Patil (GitHub: Jayyu-0011)