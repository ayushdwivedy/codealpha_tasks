import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from pathlib import Path
BASE_URL="https://books.toscrape.com/"
OUTPUT=Path("../02_dataset/books_dataset.csv")
def soup(url):
    r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=20); r.raise_for_status()
    return BeautifulSoup(r.text,"html.parser")
def scrape(max_pages=5):
    rows=[]; url=BASE_URL
    for page in range(1,max_pages+1):
        s=soup(url)
        for c in s.select("article.product_pod"):
            a=c.select_one("h3 a"); p=c.select_one(".price_color"); rt=c.select_one("p.star-rating")
            av=c.select_one(".availability"); im=c.select_one("img")
            word=next((x for x in (rt.get("class",[]) if rt else []) if x!="star-rating"),"")
            rows.append({"title":a.get("title","").strip() if a else "",
                         "price_gbp":p.get_text(strip=True) if p else "",
                         "rating":word,"availability":av.get_text(" ",strip=True) if av else "",
                         "product_url":urljoin(url,a.get("href","")) if a else "",
                         "image_url":urljoin(url,im.get("src","")) if im else "","page":page})
        nxt=s.select_one("li.next a")
        if not nxt: break
        url=urljoin(url,nxt.get("href",""))
    return pd.DataFrame(rows)
def clean(d):
    d=d.copy()
    d["price_gbp"]=pd.to_numeric(d["price_gbp"].astype(str).str.replace("£","",regex=False),errors="coerce")
    d["rating"]=d["rating"].map({"One":1,"Two":2,"Three":3,"Four":4,"Five":5})
    d["title"]=d["title"].astype(str).str.replace(r"\s+"," ",regex=True).str.strip()
    d["availability"]=d["availability"].astype(str).str.replace(r"\s+"," ",regex=True).str.strip()
    return d.drop_duplicates("title").dropna(subset=["title","price_gbp","rating"]).reset_index(drop=True)
if __name__=="__main__":
    d=clean(scrape(5)); OUTPUT.parent.mkdir(exist_ok=True); d.to_csv(OUTPUT,index=False)
    print("Saved",len(d),"records to",OUTPUT)
