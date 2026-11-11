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
    print(f"Sum null values: {df.isnull().sum()}")
    #visualizations
    text_columns = df.select_dtypes(include=["object","category"]).columns
    print(f"Data types:\n{df.dtypes}")
    if (len(text_columns) > 0):
        target_column = text_columns[0]
        value_counts = df[target_column].value_counts()
        #chart figure layout
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot()
        # This line is to create a horizontal bar chart using the value counts of the target column
        ax.barh(value_counts.index, value_counts.values, color="purple", edgecolor="black")
        # .plot(kind="bar", color="purple", edgecolor="black")
        plt.title(f"Distribution of Items by '{target_column}'")
        # This line is to set the x-axis label to the name of the target column instead of the default label
        plt.xlabel(target_column)
        # This line is to set the y-axis label to "Count" instead of the default label
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
        print(f"\nBar chart distribution of '{target_column}'")
    else:
        print("No columns found for visualization.")

def payment_chart(df: pd.DataFrame) -> None:
    """Payment Percentages by Item Purchased"""
    # pd.crosstab() calculates the percentage of each payment method for each item purchased.
    # Two dataframes: df["Item Purchased"] and df["Payment Method"] are the two columns used to create the crosstab.
    print(f"\nPayment Percentages by Item Purchased:")
    payment_percentages = pd.crosstab(
        df["Item Purchased"],
        df["Payment Method"],
        normalize="index"
    ) * 100
    # payment_percentages.round(1) rounds the percentages to one decimal place for better readability.
    print(payment_percentages.round(1))

def main() -> None:
    df = load()
    #print(f"{len(df)} rows, {len(df.columns)} columns")
    #print(df.head())
    #bar_graph(df)
    payment_chart(df)

