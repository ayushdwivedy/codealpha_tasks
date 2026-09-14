import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "02_dataset", "sales_eda_raw.csv")
OUT = os.path.join(BASE, "04_visualizations")
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# 01 Sales distribution
plt.figure(figsize=(8, 5))
plt.hist(df["Sales"].dropna(), bins=30)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "01_sales_distribution.png"), dpi=150)
plt.close()

# 02 Category sales
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
category_sales.plot(kind="bar")
plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "02_sales_by_category.png"), dpi=150)
plt.close()

# 03 Region sales
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 5))
region_sales.plot(kind="bar")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "03_sales_by_region.png"), dpi=150)
plt.close()

# 04 Monthly trend
monthly = df.set_index("Order_Date").resample("ME")["Sales"].sum()
plt.figure(figsize=(10, 5))
monthly.plot(marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "04_monthly_sales_trend.png"), dpi=150)
plt.close()

# 05 Discount vs sales
plt.figure(figsize=(8, 5))
plt.scatter(df["Discount"], df["Sales"], alpha=0.6)
plt.title("Discount vs Sales")
plt.xlabel("Discount")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "05_discount_vs_sales.png"), dpi=150)
plt.close()

# 06 Delivery days vs satisfaction
clean = df[["Delivery_Days", "Customer_Satisfaction"]].dropna()
plt.figure(figsize=(8, 5))
plt.scatter(clean["Delivery_Days"], clean["Customer_Satisfaction"], alpha=0.6)
plt.title("Delivery Days vs Customer Satisfaction")
plt.xlabel("Delivery Days")
plt.ylabel("Customer Satisfaction")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "06_delivery_vs_satisfaction.png"), dpi=150)
plt.close()

# 07 Customer type comparison
customer_sales = df.groupby("Customer_Type")["Sales"].mean()
plt.figure(figsize=(7, 5))
customer_sales.plot(kind="bar")
plt.title("Average Sales by Customer Type")
plt.xlabel("Customer Type")
plt.ylabel("Average Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "07_average_sales_customer_type.png"), dpi=150)
plt.close()

# 08 Unit price distribution / outliers
plt.figure(figsize=(8, 5))
plt.boxplot(df["Unit_Price"].dropna(), vert=True)
plt.title("Unit Price Outlier Check")
plt.ylabel("Unit Price")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "08_unit_price_outliers.png"), dpi=150)
plt.close()

print("All visualizations created.")
