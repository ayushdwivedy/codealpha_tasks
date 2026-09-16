from pathlib import Path
import re, pandas as pd, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"01_data/sentiment_dataset.csv"; OUT=ROOT/"02_analysis"; VIZ=ROOT/"03_visualizations"
OUT.mkdir(exist_ok=True); VIZ.mkdir(exist_ok=True)
df=pd.read_csv(DATA)

def clean_text(x):
    x=re.sub(r"https?://\S+|www\.\S+"," ",str(x).lower())
    return re.sub(r"\s+"," ",re.sub(r"[^a-z\s]"," ",x)).strip()
df["clean_text"]=df.text.map(clean_text)
df["word_count"]=df.clean_text.str.split().str.len()

# VADER if available; otherwise a reproducible fallback lexicon
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia=SentimentIntensityAnalyzer()
    method="VADER lexicon"
    df["compound"]=df.text.map(lambda x:sia.polarity_scores(x)["compound"])
    df["pos_score"]=df.text.map(lambda x:sia.polarity_scores(x)["pos"])
    df["neg_score"]=df.text.map(lambda x:sia.polarity_scores(x)["neg"])
    df["neu_score"]=df.text.map(lambda x:sia.polarity_scores(x)["neu"])
except Exception:
    pos=set("love loved excellent amazing happy great fantastic smooth reliable useful convenient impressive appreciate thankful exciting good premium".split())
    neg=set("disappointed poor cheaply regret frustrating ignored annoyed damaged unhappy terrible waste confusing incomplete failing fails bad".split())
    def lex(x):
        w=clean_text(x).split()
        return (sum(z in pos for z in w)-sum(z in neg for z in w))/max(len(w),1)
    df["compound"]=df.text.map(lex); df["pos_score"]=df.compound.clip(lower=0)
    df["neg_score"]=(-df.compound).clip(lower=0); df["neu_score"]=1-df.pos_score-df.neg_score
    method="fallback lexicon"

def classify(x):
    return "positive" if x>=.05 else "negative" if x<=-.05 else "neutral"
df["predicted_sentiment"]=df.compound.map(classify)

emotion_words={
"joy":"love loved happy amazing fantastic wonderful delighted",
"anger":"angry anger annoyed frustrating frustrated terrible ignored waste",
"sadness":"sad disappointed unhappy regret terrible",
"fear":"fear worried concern risk",
"surprise":"surprising surprised unexpected",
"gratitude":"thankful appreciate thanks",
"excitement":"exciting excited amazing fantastic",
"confusion":"confusing confusion unclear incomplete"}
emotion_words={k:set(v.split()) for k,v in emotion_words.items()}
def emotion(x):
    w=set(clean_text(x).split()); scores={k:len(w&v) for k,v in emotion_words.items()}
    best=max(scores,key=scores.get); return best if scores[best] else "neutral"
df["predicted_emotion"]=df.text.map(emotion)

df.to_csv(OUT/"sentiment_scored_dataset.csv",index=False)
df.predicted_sentiment.value_counts().rename_axis("sentiment").reset_index(name="count").to_csv(OUT/"sentiment_distribution.csv",index=False)
df.predicted_emotion.value_counts().rename_axis("emotion").reset_index(name="count").to_csv(OUT/"emotion_distribution.csv",index=False)
df.groupby("predicted_sentiment").compound.agg(["count","mean","median","min","max"]).reset_index().to_csv(OUT/"sentiment_scores_summary.csv",index=False)
df.groupby("predicted_sentiment").word_count.agg(["count","mean","median"]).reset_index().to_csv(OUT/"word_count_by_sentiment.csv",index=False)
pd.crosstab(df.sentiment,df.predicted_sentiment).to_csv(OUT/"confusion_matrix.csv")
accuracy=(df.sentiment==df.predicted_sentiment).mean()
pd.DataFrame([{"method":method,"records":len(df),"practice_label_accuracy":accuracy}]).to_csv(OUT/"model_summary.csv",index=False)

# Five charts
for f in list(VIZ.glob("*.png")): f.unlink()
c=df.predicted_sentiment.value_counts().reindex(["positive","neutral","negative"],fill_value=0)
plt.figure(figsize=(8,5)); c.plot(kind="bar"); plt.title("Sentiment Distribution"); plt.xlabel("Sentiment"); plt.ylabel("Count"); plt.tight_layout(); plt.savefig(VIZ/"01_sentiment_distribution.png",dpi=180); plt.close()
e=df.predicted_emotion.value_counts()
plt.figure(figsize=(9,5)); e.plot(kind="bar"); plt.title("Emotion Distribution"); plt.xlabel("Emotion"); plt.ylabel("Count"); plt.tight_layout(); plt.savefig(VIZ/"02_emotion_distribution.png",dpi=180); plt.close()
plt.figure(figsize=(8,5)); df.boxplot(column="compound",by="predicted_sentiment"); plt.suptitle(""); plt.title("Sentiment Score by Class"); plt.xlabel("Sentiment"); plt.ylabel("Compound Score"); plt.tight_layout(); plt.savefig(VIZ/"03_score_by_sentiment.png",dpi=180); plt.close()
plt.figure(figsize=(8,5)); df.groupby("predicted_sentiment").word_count.mean().reindex(["positive","neutral","negative"]).plot(kind="bar"); plt.title("Average Text Length by Sentiment"); plt.xlabel("Sentiment"); plt.ylabel("Average Words"); plt.tight_layout(); plt.savefig(VIZ/"04_text_length_by_sentiment.png",dpi=180); plt.close()
roll=df.sort_values("review_id").compound.rolling(15,min_periods=5).mean()
plt.figure(figsize=(8,5)); plt.plot(range(len(roll)),roll); plt.axhline(0,linestyle="--"); plt.title("Rolling Sentiment Trend"); plt.xlabel("Review Sequence"); plt.ylabel("Rolling Compound Score"); plt.tight_layout(); plt.savefig(VIZ/"05_sentiment_trend.png",dpi=180); plt.close()
print("Completed:",len(df),"records | method:",method,"| accuracy:",round(accuracy,4))
