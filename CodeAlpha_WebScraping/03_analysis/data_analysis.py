from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from scipy.stats import pearsonr, ttest_ind
ROOT=Path(__file__).resolve().parents[1]; IN=ROOT/"02_dataset/books_dataset_practice_raw.csv"; OUT=ROOT/"03_analysis"; V=ROOT/"04_visualizations"
OUT.mkdir(exist_ok=True); V.mkdir(exist_ok=True)
df=pd.read_csv(IN)
pd.DataFrame({"variable":df.columns,"data_type":[str(df[c].dtype) for c in df.columns],
"missing_values":[df[c].isna().sum() for c in df.columns],"unique_values":[df[c].nunique() for c in df.columns]}).to_csv(OUT/"data_structure.csv",index=False)
pd.DataFrame([{"rows":len(df),"columns":len(df.columns),"duplicate_rows":df.duplicated().sum(),
"duplicate_titles":df.title.duplicated().sum(),"missing_values_total":df.isna().sum().sum(),
"invalid_ratings":((~df.rating.between(1,5)).sum()),"non_positive_prices":(df.price_gbp<=0).sum()}]).to_csv(OUT/"data_quality_summary.csv",index=False)
df[["price_gbp","rating"]].describe().T.to_csv(OUT/"descriptive_statistics.csv")
df.rating.value_counts(dropna=False).sort_index().rename_axis("rating").reset_index(name="book_count").to_csv(OUT/"rating_distribution.csv",index=False)
df.availability.replace("",np.nan).fillna("Missing").value_counts().rename_axis("availability").reset_index(name="book_count").to_csv(OUT/"availability_distribution.csv",index=False)
df.groupby("rating",dropna=True).price_gbp.agg(["count","mean","median","min","max"]).reset_index().to_csv(OUT/"price_by_rating.csv",index=False)
df.groupby("page").price_gbp.agg(["count","mean","median"]).reset_index().to_csv(OUT/"page_summary.csv",index=False)
p=df.price_gbp.dropna(); q1,q3=p.quantile([.25,.75]); iqr=q3-q1
o=df[(df.price_gbp<q1-1.5*iqr)|(df.price_gbp>q3+1.5*iqr)]; o.to_csv(OUT/"price_outliers.csv",index=False)
t=df[["rating","price_gbp"]].dropna(); r,pv=pearsonr(t.rating,t.price_gbp)
pd.DataFrame([{"test":"Pearson correlation: rating vs price","null_hypothesis":"No linear relationship","correlation_r":r,"p_value":pv,"alpha":.05,"decision":"Reject H0" if pv<.05 else "Fail to reject H0"}]).to_csv(OUT/"hypothesis_test.csv",index=False)
for name,kind,title,x,y in [
("01_rating_distribution","bar","Book Rating Distribution","Rating","Number of Books"),
("02_price_distribution","hist","Book Price Distribution","Price (£)","Number of Books")]:
    plt.figure(figsize=(8,5))
    if kind=="bar": df.rating.value_counts().sort_index().plot(kind="bar")
    else: df.price_gbp.plot(kind="hist",bins=12)
    plt.title(title); plt.xlabel(x); plt.ylabel(y); plt.tight_layout(); plt.savefig(V/(name+".png"),dpi=160); plt.close()
plt.figure(figsize=(8,5)); plt.scatter(df.rating,df.price_gbp,alpha=.7); plt.title("Rating vs Price"); plt.xlabel("Rating"); plt.ylabel("Price (£)"); plt.tight_layout(); plt.savefig(V/"03_rating_vs_price.png",dpi=160); plt.close()
plt.figure(figsize=(8,5)); df.availability.replace("",np.nan).fillna("Missing").value_counts().plot(kind="bar"); plt.title("Availability Status"); plt.xlabel("Availability"); plt.ylabel("Number of Books"); plt.tight_layout(); plt.savefig(V/"04_availability.png",dpi=160); plt.close()
plt.figure(figsize=(8,5)); df.groupby("page").price_gbp.mean().plot(marker="o"); plt.title("Average Price by Scraped Page"); plt.xlabel("Page"); plt.ylabel("Average Price (£)"); plt.tight_layout(); plt.savefig(V/"05_average_price_by_page.png",dpi=160); plt.close()
print("Analysis complete. Correlation:",round(r,4),"p-value:",pv,"Outliers:",len(o))
