import os
import pandas as pd
import numpy as np

from scipy.stats import ttest_ind, pearsonr

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "02_dataset", "sales_eda_raw.csv")
OUT = os.path.join(BASE, "03_analysis")
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# 1. Data structure
structure = pd.DataFrame({
    "Variable": df.columns,
    "Data_Type": [str(df[c].dtype) for c in df.columns],
    "Missing_Values": [int(df[c].isna().sum()) for c in df.columns],
    "Unique_Values": [int(df[c].nunique(dropna=True)) for c in df.columns],
})
structure.to_csv(os.path.join(OUT, "01_data_structure.csv"), index=False)

# 2. Descriptive statistics
numeric = df.select_dtypes(include=np.number)
desc = numeric.describe().T
desc["missing_values"] = numeric.isna().sum()
desc.to_csv(os.path.join(OUT, "02_descriptive_statistics.csv"))

# 3. Category summaries
category_summary = (
    df.groupby("Category", dropna=False)
      .agg(
          Orders=("Order_ID", "count"),
          Total_Sales=("Sales", "sum"),
          Average_Sales=("Sales", "mean"),
          Average_Quantity=("Quantity", "mean"),
          Average_Satisfaction=("Customer_Satisfaction", "mean")
      )
      .reset_index()
)
category_summary.to_csv(os.path.join(OUT, "03_category_summary.csv"), index=False)

# 4. Region summaries
region_summary = (
    df.groupby("Region")
      .agg(
          Orders=("Order_ID", "count"),
          Total_Sales=("Sales", "sum"),
          Average_Sales=("Sales", "mean"),
          Average_Delivery_Days=("Delivery_Days", "mean")
      )
      .reset_index()
)
region_summary.to_csv(os.path.join(OUT, "04_region_summary.csv"), index=False)

# 5. Monthly trend
monthly = (
    df.set_index("Order_Date")
      .resample("ME")
      .agg(Orders=("Order_ID", "count"), Total_Sales=("Sales", "sum"), Average_Sales=("Sales", "mean"))
      .reset_index()
)
monthly["Month"] = monthly["Order_Date"].dt.strftime("%Y-%m")
monthly.to_csv(os.path.join(OUT, "05_monthly_sales_trend.csv"), index=False)

# 6. Data quality checks
duplicate_count = int(df.duplicated().sum())
missing = df.isna().sum().reset_index()
missing.columns = ["Column", "Missing_Values"]

# IQR outlier detection
outlier_rows = []
for col in ["Sales", "Unit_Price", "Delivery_Days"]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    count = int(((df[col] < lower) | (df[col] > upper)).sum())
    outlier_rows.append([col, q1, q3, lower, upper, count])

outliers = pd.DataFrame(
    outlier_rows,
    columns=["Variable", "Q1", "Q3", "Lower_Bound", "Upper_Bound", "Outlier_Count"]
)

quality = {
    "Total_Rows": len(df),
    "Total_Columns": len(df.columns),
    "Duplicate_Rows": duplicate_count,
    "Rows_With_Any_Missing_Value": int(df.isna().any(axis=1).sum()),
}
pd.DataFrame([quality]).to_csv(os.path.join(OUT, "06_data_quality_overview.csv"), index=False)
missing.to_csv(os.path.join(OUT, "07_missing_values.csv"), index=False)
outliers.to_csv(os.path.join(OUT, "08_outlier_detection.csv"), index=False)

# 7. Hypothesis test:
# H0: Average sales for returning customers = average sales for new customers
# H1: Average sales differ between the two groups
new_sales = df.loc[df["Customer_Type"] == "New", "Sales"].dropna()
returning_sales = df.loc[df["Customer_Type"] == "Returning", "Sales"].dropna()
t_stat, p_value = ttest_ind(new_sales, returning_sales, equal_var=False)

hypothesis = pd.DataFrame([{
    "Hypothesis": "Average Sales: New vs Returning Customers",
    "Null_Hypothesis": "There is no difference in average sales between the two customer types.",
    "Alternative_Hypothesis": "Average sales are different between the two customer types.",
    "New_Customer_Mean_Sales": new_sales.mean(),
    "Returning_Customer_Mean_Sales": returning_sales.mean(),
    "T_Statistic": t_stat,
    "P_Value": p_value,
    "Significance_Level": 0.05,
    "Conclusion": "Reject H0" if p_value < 0.05 else "Fail to reject H0"
}])
hypothesis.to_csv(os.path.join(OUT, "09_hypothesis_test.csv"), index=False)

# 8. Correlation test:
# Sales vs Customer Satisfaction
corr_df = df[["Sales", "Customer_Satisfaction"]].dropna()
corr, corr_p = pearsonr(corr_df["Sales"], corr_df["Customer_Satisfaction"])
correlation = pd.DataFrame([{
    "Variable_1": "Sales",
    "Variable_2": "Customer_Satisfaction",
    "Pearson_Correlation": corr,
    "P_Value": corr_p
}])
correlation.to_csv(os.path.join(OUT, "10_correlation_test.csv"), index=False)

print("EDA completed successfully.")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Duplicate rows:", duplicate_count)
print("Hypothesis test p-value:", p_value)
