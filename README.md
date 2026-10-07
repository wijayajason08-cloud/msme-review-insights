# BukuWarung Feedback Insights — NLP-Driven Pain Point Analysis & Classifier

> Status: MVP complete

This project scrapes, analyzes, and models user reviews of the MSME bookkeeping app **BukuWarung** on the Google Play Store to identify concrete, data-backed user pain points — then turns those findings into a working tool: a sentiment and pain-point classifier for new, unrated feedback text.

## Background

BukuWarung and KasirPintar reviews (8,000 raw reviews from both apps) were scraped and analyzed to find common MSME-app complaints. Early analysis revealed a severe confound: 91% of negative reviews came from BukuWarung, while KasirPintar was only 6.9% negative. All pain-point conclusions below are therefore scoped to **BukuWarung only** — see `docs/data-limitations.md` for the full reasoning.

## Key Findings

Five recurring pain points were identified by cross-validating two independent NLP methods (bigram distinctiveness analysis and LDA topic modeling), then quantified against all 1,767 negative BukuWarung reviews:

| Pain Point | Share of Negative Reviews |
|---|---|
| Saldo/QRIS/verification issues | 17.3% |
| Slow customer service response | 10.9% |
| UI bug: "0" button covered by navigation bar | 8.4% |
| App crashes / force-closes | 5.1% |
| Data/records lost | 5.0% |

Full analysis, methodology, and supporting quotes: [`docs/problem-statement.md`](docs/problem-statement.md).

## Methodology

1. **Scraping** — `google-play-scraper`, 4,000 reviews per app
2. **Preprocessing** — clause-aware text cleaning with negation-safe stopword removal (custom-built after a library bug was found to silently invert sentiment — see Key Learnings)
3. **EDA** — rating distribution, wordclouds
4. **Keyword & Topic Analysis** — bigram distinctiveness scoring + LDA, cross-validated against each other
5. **Sentiment Modeling** — Logistic Regression (TF-IDF features), validated in-domain and cross-app to check the model generalizes rather than just memorizing app identity
6. **Problem Statement** — pain points ranked and quantified with real review evidence
7. **Prototype** — a Streamlit tool applying the trained model to new feedback text

## Features (MVP)

- **Text input** — paste any feedback/review text
- **Sentiment prediction** — positif/negatif with confidence score
- **Pain-point category detection** — flags which of the 5 validated categories the text matches
- **Session history table** — running log of analyzed feedback

Full MVP scope and rationale: [`docs/mvp-scope.md`](docs/mvp-scope.md).

## Demo

<!-- TODO: add screenshot/GIF -->

- **Live app:** _(link added after deployment)_
- **Video walkthrough:** _(link added after recording)_

## Tech Stack

- Python
- `google-play-scraper` — review data collection
- `scikit-learn` — TF-IDF, Logistic Regression, LDA topic modeling
- `pandas` — data wrangling
- `matplotlib` / `wordcloud` — visualization
- `Streamlit` — application interface
- `pytest` — unit testing

## Getting Started

```bash
# Clone the repo
git clone https://github.com/wijayajason08-cloud/umkm-review-insights.git
cd umkm-review-insights

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/app.py
# On Windows, if the `streamlit` command isn't recognized:
# python -m streamlit run src/app.py
```

## Project Structure

```
umkm-review-insights/
├── data/
│   ├── raw/                     # scraped review data
│   └── processed/               # cleaned data
├── src/
│   ├── scraper.py               # Step 2: data collection
│   ├── id_stopwords.py          # centralized stopword list (negation-safe)
│   ├── text_cleaning.py         # shared text cleaning (training + inference)
│   ├── preprocessing.py         # Step 3: data cleaning
│   ├── eda.py                   # Step 4: exploratory analysis
│   ├── keyword_analysis.py      # Step 4: distinctive keyword/bigram analysis
│   ├── data_diagnostics.py      # bias/confound checks
│   ├── check_preprocessing.py   # preprocessing verification utility
│   ├── inspect_phrase.py        # quick review-lookup utility
│   ├── sentiment_model.py       # Step 5: sentiment classifier
│   ├── topic_modeling.py        # Step 5: LDA topic modeling
│   ├── pain_point_categories.py # centralized pain-point category definitions
│   ├── problem_statement_helper.py  # Step 6: pain-point quantification
│   ├── feedback_classifier.py   # Step 8: MVP core logic
│   └── app.py                   # Step 9: Streamlit UI
├── models/                      # trained sentiment model + vectorizer
├── docs/
│   ├── images/                  # charts and wordclouds
│   ├── data-sources.md          # target app selection rationale
│   ├── data-limitations.md      # known limitations + debugging log
│   ├── topic-modeling-results.md
│   ├── problem-statement.md     # ranked, quantified pain points
│   └── mvp-scope.md             # MVP feature scope and rationale
├── tests/
│   └── test_classifier.py
├── requirements.txt
└── README.md
```

## Key Learnings

This project surfaced and fixed three non-obvious bugs during development, documented in full in `docs/data-limitations.md` (Section 8):

1. **A stopword-removal library silently inverted sentiment** — "tetap tidak bisa" became "tetap bisa" — found by comparing word counts before/after cleaning, not by assuming a popular library was correct.
2. **Bigram generation could pair words across unrelated clauses** — fixed by preserving original punctuation as clause boundaries before cleaning.
3. **A sample-weighting scheme meant to fix an app-level class imbalance instead amplified the influence of 2 mislabeled reviews** — found by reading the actual reviews behind a model's top coefficients instead of trusting the ranking at face value.

Each fix was driven by inspecting raw data and predictions directly rather than trusting intermediate output.

## Limitations

See [`docs/data-limitations.md`](docs/data-limitations.md) for the full discussion, including: app-level confounding between BukuWarung and KasirPintar, label noise from using star ratings as a sentiment proxy, and the scope restriction of all findings to BukuWarung.

## Roadmap

<!-- TODO: fill in future development ideas -->
- Expand analysis to more MSME finance apps once a larger, comparably sized negative sample is available
- Replace keyword-based category detection with a trained multi-label classifier

## Credits

Review data collected from the Google Play Store via the `google-play-scraper` library.
