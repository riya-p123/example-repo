from importlib.resources import files
from pathlib import Path
import pandas as pd


def load() -> pd.DataFrame:
    """Load the survey dataset as a DataFrame."""
    # __init__.py -> example_repo -> src -> example-repo
    root_dir = Path(__file__).resolve().parent.parent.parent
    path = root_dir/ "data" / "Fashion_Retail_Sales.csv"
    with path.open("rb") as f:
        return pd.read_csv(f)


def main() -> None:
    df = load()
    print(f"{len(df)} rows, {len(df.columns)} columns")
    print(df.head())
