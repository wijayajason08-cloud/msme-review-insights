# Data Cleaning & Preprocessing Notes

This document briefly explains the cleaning steps applied to the raw review dataset.

## Pipeline

1. **Deduplication** — removed exact duplicate reviews (same `content` text)
2. **Empty review removal** — dropped rows with missing or blank review text
3. **Text cleaning** — lowercased all text, removed URLs, numbers, punctuation, and emoji
4. **Slang normalization** — common Indonesian informal words/abbreviations (e.g., "gk" → "tidak", "bgt" → "banget") converted to their standard form using a custom dictionary
5. **Stopword removal** — removed common Indonesian stopwords using the `Sastrawi` library
6. **Post-cleaning empty removal** — dropped rows that became empty after cleaning (e.g., reviews that were only emoji or numbers)

## Results

- Raw dataset size: 8000 rows
- Cleaned dataset size: 6352 rows
- Rows removed: 1648 (duplicates + empty + post-cleaning empty)

## Known Limitations

- The slang dictionary is manually curated and may not cover all informal words present in the data
- No language detection was applied — a small number of non-Indonesian reviews may remain in the dataset
- Stopword removal uses a general-purpose Indonesian list, which may occasionally remove words that carry sentiment meaning in this specific domain (e.g., "tidak" is preserved intentionally since Sastrawi's default list does not treat it as a stopword, but this should be double-checked during the sentiment analysis stage in Step 5)
