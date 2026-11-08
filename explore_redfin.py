# ------------------------------------------------------------
# explore_redfin.py: scratch pad for looking at a new CSV
#
# WHAT IT DOES
#   Prints shape, types, and blanks for a Redfin download, so
#   you can spot surprises before importing.
#
# USED BY
#   Nothing. It isn't part of the app. Edit it freely.
#   Handy when you download a new ZIP code.
# ------------------------------------------------------------

import pandas as pd

df = pd.read_csv(
    "data/inbox/redfin_39157_2026-11-04.csv.csv",
    dtype={"ZIP OR POSTAL CODE": str},
)
df = df.dropna(subset=["ADDRESS"])

print("Rows, columns:", df.shape)
print()
print(df[["ADDRESS", "PRICE", "BEDS", "BATHS", "ZIP OR POSTAL CODE"]].head())
print()
print(df.dtypes)
print()
print(df.isna().sum())