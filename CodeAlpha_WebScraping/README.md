**Web Scraping, Exploratory Data Analysis & Statistical Validation**

**Source:** Books to Scrape — https://books.toscrape.com/

> Dataset note: the packaging environment cannot access the public internet. The included `books_dataset_practice_raw.csv` is a clearly labeled practice dataset for demonstrating the complete analysis workflow. Run the scraper on an internet-connected computer to generate live scraped data.

## 1. Meaningful questions
- What is the average, minimum and maximum book price?
- Which rating is most common?
- Is rating related to price?
- Are there unusual prices?
- Are records missing, duplicated or invalid?
- Are variables stored in suitable data types?
- Does availability differ across the dataset?
- Does average price vary by scraped page?

## 2. Data structure
The project checks rows, columns, variables, data types, missing values and unique values. Results: `03_analysis/data_structure.csv`.

## 3. Trends, patterns and anomalies
The project analyzes rating distribution, price distribution, price by rating, availability, page-level price patterns and IQR price outliers.

## 4. Hypothesis testing
**H0:** There is no linear relationship between book rating and price.  
**H1:** There is a linear relationship.

Pearson correlation: **0.0467**  
p-value: **0.6459**  
Alpha: **0.05**  
Decision: **Fail to reject H0**

The scatter plot is `04_visualizations/03_rating_vs_price.png`. Correlation does not establish causation.

## 5. Data-quality findings
- Rows: 100
- Columns: 7
- Duplicate rows: 0
- Duplicate titles: 1
- Missing values: 102
- Invalid ratings: 1
- Non-positive prices: 0

Potential price outliers are listed in `price_outliers.csv`. Outliers should be checked against the original webpage rather than automatically deleted.

## 6. Method
Requests downloads HTML, BeautifulSoup parses HTML and CSS selectors extract fields. Pagination follows the site's Next link. Pandas cleans and structures the dataset. Matplotlib creates visualizations and SciPy performs statistical tests.

## 7. Deliverables
- `01_web_scraping/scrape_books.py`
- `01_web_scraping/requirements.txt`
- `02_dataset/books_dataset_practice_raw.csv`
- `03_analysis/data_analysis.py`
- Analysis CSV files
- Five PNG visualizations
- This report and README

## 8. Run
```bash
cd 01_web_scraping
pip install -r requirements.txt
python scrape_books.py
cd ../03_analysis
python data_analysis.py
```

## 9. Conclusion
This project covers the complete internship workflow: asking analytical questions, exploring structure, identifying patterns and anomalies, testing a hypothesis with statistics and visualization, and detecting data-quality problems. The workflow can be extended in Excel or Power BI for further analysis.

## 10. Responsible scraping
Use public information responsibly. Respect terms of service, robots.txt guidance, rate limits, privacy requirements and applicable laws. Never bypass authentication or technical restrictions.


See the Python files for the implementation.
