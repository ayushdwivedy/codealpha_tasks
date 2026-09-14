# PROJECT REPORT
# Exploratory Data Analysis of Retail Sales Data

## 1. Introduction
Exploratory Data Analysis (EDA) is the process of understanding a dataset before applying advanced statistical models or machine learning algorithms. In this project, a retail sales dataset is explored to understand its structure, trends, relationships and possible data-quality problems.

## 2. Objectives
1. Ask meaningful questions before analysis.
2. Understand the structure and data types of the dataset.
3. Identify trends and patterns.
4. Detect anomalies, missing values and duplicates.
5. Use statistics to test a business hypothesis.
6. Use visualizations to validate observations.
7. Prepare the dataset for future analysis or machine learning.

## 3. Questions Asked
- Which category has the highest sales?
- Which region generates the most sales?
- What is the monthly sales trend?
- Do returning customers have different average sales from new customers?
- Is delivery time related to customer satisfaction?
- What effect does discount appear to have on sales?
- Are there missing, duplicate or unusual records?

## 4. Data Structure
The dataset contains order-level records with categorical, numerical and date variables.

Examples:
- Categorical: Region, Category, Customer_Type, Payment_Method
- Numerical: Quantity, Unit_Price, Discount, Sales, Delivery_Days, Customer_Satisfaction
- Date: Order_Date
- Identifier: Order_ID

The detailed data structure is stored in:
`03_analysis/01_data_structure.csv`

## 5. Descriptive Analysis
Descriptive statistics were calculated for numerical variables. Measures such as count, mean, standard deviation, minimum, maximum and quartiles help understand the distribution of the data.

Output:
`03_analysis/02_descriptive_statistics.csv`

## 6. Trends and Patterns
Category-wise, region-wise and month-wise sales were analyzed. These summaries help identify high-performing product categories, stronger regions and changes in sales over time.

Outputs:
- `03_analysis/03_category_summary.csv`
- `03_analysis/04_region_summary.csv`
- `03_analysis/05_monthly_sales_trend.csv`

## 7. Data Quality Checks
The dataset was checked for:
- Missing values
- Duplicate rows
- Potential outliers
- Unusual delivery times
- Extreme unit prices

The raw dataset intentionally includes a few issues so that the EDA workflow demonstrates how such problems can be detected.

Outputs:
- `03_analysis/06_data_quality_overview.csv`
- `03_analysis/07_missing_values.csv`
- `03_analysis/08_outlier_detection.csv`

## 8. Hypothesis Testing
### Hypothesis
**Null Hypothesis (H0):** There is no difference in average sales between new and returning customers.

**Alternative Hypothesis (H1):** Average sales are different between new and returning customers.

An independent two-sample t-test was used with a significance level of 0.05.

The result is saved in:
`03_analysis/09_hypothesis_test.csv`

Interpretation:
- If p-value < 0.05, reject H0.
- If p-value >= 0.05, fail to reject H0.

## 9. Correlation Analysis
Pearson correlation was calculated between Sales and Customer Satisfaction to check whether the two numerical variables have a linear relationship.

Output:
`03_analysis/10_correlation_test.csv`

Correlation does not prove causation; it only describes the strength and direction of a linear relationship.

## 10. Visualizations
The project includes:
1. Sales distribution
2. Sales by category
3. Sales by region
4. Monthly sales trend
5. Discount vs sales
6. Delivery days vs customer satisfaction
7. Average sales by customer type
8. Unit-price outlier check

## 11. Conclusion
EDA provides an initial understanding of the retail sales dataset and identifies issues that should be handled before further modeling. The analysis combines descriptive statistics, data-quality checks, hypothesis testing and visualization. The cleaned and validated dataset could later be used for dashboards, predictive analysis or machine learning.

## 12. Future Scope
- Clean and preprocess the dataset.
- Build a sales prediction model.
- Create a Power BI dashboard.
- Perform customer segmentation.
- Analyze seasonal patterns.
- Predict customer satisfaction.
