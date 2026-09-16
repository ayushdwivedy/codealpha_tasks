# Sentiment Analysis Internship Project

## Overview
An end-to-end NLP project that classifies text as **positive, negative, or neutral**, detects emotions using lexicons, analyzes sentiment patterns, and produces visual insights.

## Internship Requirements
1. **Sentiment classification:** Positive / negative / neutral classification using a lexicon-based NLP method.
2. **Emotion detection:** Lexicon matching for joy, anger, sadness, fear, surprise, gratitude, excitement, and confusion.
3. **Source workflow:** The project structure is suitable for public reviews, social-media posts, or news text. The included data is explicitly a **synthetic practice dataset**, not real Amazon/social/news data.
4. **Opinion/trend analysis:** Sentiment proportions, emotion frequencies, sentiment scores, text length, and rolling trends are analyzed.
5. **Practical insights:** Findings can support marketing, product development, customer feedback analysis, and social insights.

## Meaningful Questions
- What percentage of text is positive, neutral, or negative?
- Which emotions occur most often?
- How strong are the sentiment scores?
- Does sentiment change across the review sequence?
- Are negative texts longer than positive texts?
- What recurring emotions or negative themes may need attention?

## NLP Pipeline
Text → cleaning → tokenization/word matching → lexicon scoring → sentiment class → emotion detection → statistics → visualization → insights.

## Method
The code uses **VADER** when available; otherwise it uses a small built-in fallback lexicon. VADER-style thresholds are used: compound >= 0.05 = positive, <= -0.05 = negative, otherwise neutral.

## Dataset
Records: **144**

The dataset is synthetic practice data written in a public-review style. It is provided so the complete project can run reproducibly without falsely claiming that real Amazon or social-media data was downloaded.

## Evaluation
Practice-label accuracy: **94.44%**

This metric is only an educational demonstration on the included labels. Real-world performance should be measured on an independently labeled test set.

## Outputs
- `sentiment_scored_dataset.csv`
- `sentiment_distribution.csv`
- `emotion_distribution.csv`
- `sentiment_scores_summary.csv`
- `word_count_by_sentiment.csv`
- `confusion_matrix.csv`
- `model_summary.csv`
- Five PNG visualizations

## Data Quality Checks
Before using real data, check missing text, duplicates, spam, very short texts, language consistency, class imbalance, sarcasm, context, privacy/PII, collection date, and source permissions.

## Practical Use
**Marketing:** measure customer reaction to campaigns.  
**Product development:** identify recurring negative feedback.  
**Customer support:** surface strongly negative messages.  
**Social insights:** monitor changes in public tone over time.

## Limitations
Lexicon-based methods can struggle with sarcasm, mixed sentiment, slang, domain-specific vocabulary, and context. Results should be treated as analytical signals rather than perfect judgments.

## Run
```bash
pip install -r 02_analysis/requirements.txt
python 02_analysis/sentiment_analysis.py
```

## Responsible Data Use
For Amazon reviews, social media, or news, use data only where collection and use are permitted. Respect terms of service, privacy requirements, rate limits, and applicable laws.
