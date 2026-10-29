from importlib.resources import files

import pandas as pd


def load() -> pd.DataFrame:
    """Load the survey dataset as a DataFrame."""
    path = files("data\Fashion_Retail_Sales.csv")
    with path.open("rb") as f:
        return pd.read_csv(f)


def main() -> None:
    df = load()
    print(f"{len(df)} rows, {len(df.columns)} columns")
    print(df.head())
