from importlib.resources import files
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load() -> pd.DataFrame:
    """Load the survey dataset as a DataFrame."""
    # __init__.py -> example_repo -> src -> example-repo
    root_dir = Path(__file__).resolve().parent.parent.parent
    path = root_dir/ "data" / "Fashion_Retail_Sales.csv"
    with path.open("rb") as f:
        return pd.read_csv(f)

def bar_graph(df: pd.DataFrame) -> None:
    """Graph the dataset."""
    print("\n=== Data Summary ===")
    print(df.info())
    #check sum on null values in each column
    print(df.isnull().sum())
    #visualizations
    text_columns = df.select_dtypes(include=["object","category"]).columns
    if (len(text_columns) >0):
        target_column = text_columns[0]
        print(f"\nBar chart distribution of '{target_column}'")
        #chart figure layout
        plt.figure(figsize=(10,6))
        df[target_column].value_counts().plot(kind="bar", color="purple", edgecolor="black")
        plt.title(f"Distribution of Items by '{target_column}'")
        plt.xlabel(target_column)
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
    else:
        print("No columns found for visualization.")

# def pie_chart(df: pd.DataFrame) -> None:

def main() -> None:
    df = load()
    #print(f"{len(df)} rows, {len(df.columns)} columns")
    #print(df.head())
    bar_graph(df)

