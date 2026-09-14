# Exploratory Data Analysis (EDA) Internship Project

## Project Title
**Exploratory Data Analysis of Retail Sales Data**

## Objective
The goal of this project is to explore a retail sales dataset before performing advanced analysis or machine learning.

This project covers:
- Asking meaningful questions before analysis
- Understanding variables and data types
- Finding trends and patterns
- Detecting anomalies and outliers
- Testing a hypothesis using statistics
- Validating assumptions with visualizations
- Identifying missing values and duplicate records
- Documenting data-quality issues

## Dataset
The raw dataset is available in:
`02_dataset/sales_eda_raw.csv`

It contains order information such as:
- Order ID
- Order Date
- Region
- Category
- Customer Type
- Payment Method
- Quantity
- Unit Price
- Discount
- Sales
- Delivery Days
- Customer Satisfaction

## Project Structure

```text
📁 eda-internship-project
│
├── 📁 01_eda
│   ├── eda_analysis.py
│   ├── visualizations.py
│   ├── eda_questions.md
│   └── requirements.txt
│
├── 📁 02_dataset
│   └── sales_eda_raw.csv
│
├── 📁 03_analysis
│   ├── 01_data_structure.csv
│   ├── 02_descriptive_statistics.csv
│   ├── 03_category_summary.csv
│   ├── 04_region_summary.csv
│   ├── 05_monthly_sales_trend.csv
│   ├── 06_data_quality_overview.csv
│   ├── 07_missing_values.csv
│   ├── 08_outlier_detection.csv
│   ├── 09_hypothesis_test.csv
│   └── 10_correlation_test.csv
│
├── 📁 04_visualizations
│   ├── 01_sales_distribution.png
│   ├── 02_sales_by_category.png
│   ├── 03_sales_by_region.png
│   ├── 04_monthly_sales_trend.png
│   ├── 05_discount_vs_sales.png
│   ├── 06_delivery_vs_satisfaction.png
│   ├── 07_average_sales_customer_type.png
│   └── 08_unit_price_outliers.png
│
├── PROJECT_REPORT.md
└── README.md
```

## How to Run

### 1. Install requirements
```bash
pip install -r 01_eda/requirements.txt
```

### 2. Run analysis
```bash
python 01_eda/eda_analysis.py
```

### 3. Generate visualizations
```bash
python 01_eda/visualizations.py
```

## Key EDA Techniques Used
- `head()`, `info()`, `describe()`
- Missing-value analysis
- Duplicate detection
- GroupBy aggregation
- Monthly trend analysis
- IQR-based outlier detection
- Histogram
- Bar chart
- Scatter plot
- Box plot
- Independent two-sample t-test
- Pearson correlation

## Important Note
The dataset intentionally contains a small number of missing values, duplicate rows, and unusual observations. This is done so the EDA process demonstrates how data problems are detected before further analysis.
