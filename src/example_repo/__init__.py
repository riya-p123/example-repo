from importlib.resources import files
from pathlib import Path
from scipy.stats import chi2_contingency
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
    # select_dtypes() method is used to select columns of a specific data type from the DataFrame. In this case, it selects columns with data types "object" and "category", which are typically used for text data. The resulting columns are stored in the variable text_columns.
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

def payment_chart(df: pd.DataFrame) -> pd.DataFrame:
    """Plot Payment Percentages by Item Purchased"""
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
    return payment_percentages
    
def payment_percentages_plot(payment_percentages:pd.DataFrame) -> None:
    # payment_percentages.plot() creates a bar chart to visualize the payment percentages by item purchased 
    # payment_percentages is the pandas dataframe created earlier
    ax = payment_percentages.plot(
        kind="bar",
        # stacked=True puts the payment methods on top of each other in the bar chart, making it easier to compare the total percentages for each item purchased.
        stacked=True,
        figsize=(10, 6)
    )

    ax.set_title("Payment Percentages by Item Purchased")
    ax.set_xlabel("Item Purchased")
    ax.set_ylabel("Percentage of purchases")
    # set_ylim(0, 100) sets the y-axis limits to be between 0 and 100, which is reasonable for the given dataset
    ax.set_ylim(0, 100)

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")
    # Add a legend to the chart to indicate which color corresponds to which payment method
    plt.legend(title="Payment Method")
    # tight_layout() adjusts the layout of the chart to make sure that all elements fit within the figure area and are not cut off.
    plt.tight_layout()
    plt.show()

def payment_chi_squared(df: pd.DataFrame) -> None:
    """Perform Chi-Squared Test for Independence on Payment Method and Item Purchased"""
    # data is a new DataFrame that contains only the "Payment Method" and "Item Purchased" columns from the original DataFrame df, with any rows containing missing values dropped.
    data = df[["Payment Method", "Item Purchased"]].dropna()
    print(f"Rows excluded for missing values: {len(df) -len(data)}")
    # pd.crosstab() creates a contingency table (cross-tabulation) of the counts of occurrences for each combination of "Item Purchased" and "Payment Method". The resulting table is stored in the variable counts.
    counts = pd.crosstab(data["Item Purchased"], data["Payment Method"])
    # Perform the Chi-Squared test
    # chi2_contingency() function from the scipy.stats module is used to perform the Chi-Squared test for independence on the contingency table counts. 
    # It returns four values: chi2 (the Chi-Squared statistic), p_value (the p-value of the test), dof (degrees of freedom), and expected (the expected frequencies if the null hypothesis is true).
    chi2, p_value, dof, expected = chi2_contingency(counts)
    print(f"Chi-Squared Statistic: {chi2}")
    print(f"P-Value: {p_value}")
    print(f"Degrees of Freedom: {dof}")
    # Create a DataFrame for the expected frequencies with the same index and columns as the counts DataFrame
    expected_table = pd.DataFrame(expected, index=counts.index, columns=counts.columns)
    print("\nExpected counts if the variables were independent:")
    # expected_table.round(2) rounds the expected counts to two decimal places for better readability.
    print(expected_table.round(2))
    # Check for expected counts below 5
    print(f"\nCells with expected counts below 5: {(expected_table < 5).sum()}")

def main() -> None:
    df = load()
    #print(f"{len(df)} rows, {len(df.columns)} columns")
    #print(df.head())
    #bar_graph(df)
    #payment_chart(df)
    #percentages = payment_chart(df)
    #payment_percentages_plot(percentages)
    payment_chi_squared(df)
