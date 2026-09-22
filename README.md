# UMKM Pulse — Uncovering MSME Financial Pain Points via NLP Review Mining

> Status: Work in Progress

This project analyzes user reviews of MSME (micro, small, and medium enterprise) financial apps (e.g., BukuWarung, BukuKas) on the Google Play Store using NLP to uncover real, data-backed pain points — then builds a lightweight prototype addressing the top issue.

## Background

<!-- TODO: fill in after Step 6 (Insight Synthesis) — summary of the problem statement + 1–2 wordcloud/chart visualizations -->

## Methodology

1. **Scraping** — collecting reviews from several MSME financial apps on the Play Store
2. **Preprocessing** — Indonesian-language text cleaning (stopword removal, slang normalization)
3. **Sentiment Analysis** — classifying reviews as positive/negative
4. **Topic Modeling** — clustering complaints into key themes (LDA)
5. **Insight Synthesis** — summarizing the top pain points backed by data
6. **Prototype Development** — building a lightweight solution based on the findings

## Features

<!-- TODO: fill in once the MVP scope is finalized (Step 7) -->
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

## Demo

<!-- TODO: add a screenshot/GIF once the UI is complete (Step 9) -->

## Tech Stack

- Python
- `google-play-scraper` — review data collection
- `Sastrawi` — Indonesian NLP preprocessing
- `scikit-learn` — sentiment analysis
- `gensim` — topic modeling (LDA)
- `matplotlib` / `wordcloud` — visualization
- `Streamlit` — application interface

## Getting Started

```bash
# Clone the repo
git clone https://github.com/<your-username>/umkm-review-insights.git
cd umkm-review-insights

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/app.py
```

## Live Demo & Video

<!-- TODO: add Streamlit deployment link and YouTube demo video link -->

- Live Demo: _(coming soon)_
- Video Demo: _(coming soon)_

## Project Structure

```
umkm-review-insights/
├── data/
│   ├── raw/            # raw scraped review data
│   └── processed/      # cleaned data
├── src/                # core code (scraper, preprocessing, model, app)
├── notebooks/          # exploration notebooks (EDA, NLP experiments)
├── docs/               # supporting documents (problem statement, MVP scope)
├── tests/              # unit tests
└── README.md
```

## Roadmap

<!-- TODO: outline future development ideas, e.g. analyzing additional apps, predictive features, etc. -->

## Credits

Review data collected from the Google Play Store via the `google-play-scraper` library.
