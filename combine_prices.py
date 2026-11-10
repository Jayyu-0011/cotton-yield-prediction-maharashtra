import csv, glob, os, re
import pandas as pd

rows, problems = [], []
for path in sorted(glob.glob(os.path.join("data", "raw", "*.csv"))):
    with open(path, encoding="utf-8-sig", newline="") as f:
        lines = list(csv.reader(f))
    title = " ".join(lines[0]) if lines else ""
    m = re.search(r"on:\s*(\d{1,2}-[A-Za-z]{3}-\d{4})", title)
    if not m:
        problems.append((os.path.basename(path), "date not found in file"))
        continue
    date = pd.to_datetime(m.group(1), format="%d-%b-%Y")

    in_mh, found = False, False
    for r in lines:
        if not r:
            continue
        first = r[0].strip()
        if first.startswith("State/UT Name"):
            in_mh = "Maharashtra" in first
        elif in_mh and first == "Total":
            rows.append({"date": date,
                         "arrivals_tonnes": float(r[1]),
                         "avg_modal_price": float(r[6])})
            found = True
            in_mh = False
    if not found:
        problems.append((date.strftime("%Y-%m-%d"), "No Maharashtra data"))

df = pd.DataFrame(rows).drop_duplicates("date").sort_values("date")
os.makedirs(os.path.join("data", "processed"), exist_ok=True)
df.to_csv(os.path.join("data", "processed", "maharashtra_price.csv"), index=False)
print(df.to_string(index=False))
print("\nTotal dates:", len(df))
print("Problems:", problems)