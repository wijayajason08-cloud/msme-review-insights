# Data Limitations

This document records known limitations of the dataset and how the analysis accounts for them.

## 1. Severe imbalance between apps and sentiment

| App | Negative | Positive | Total | % Negative |
|---|---|---|---|---|
| BukuWarung | 1,767 | 1,554 | 3,321 | 53.2% |
| KasirPintar | 177 | 2,387 | 2,564 | 6.9% |

About 91% of all negative reviews (1,767 of 1,944) come from BukuWarung. A model trained on pooled data can score well simply by recognizing app-specific vocabulary instead of genuine sentiment. Keyword findings on pooled data can also reflect app-specific features rather than shared pain points.

**Mitigations:** keyword analysis is compared between pooled and BukuWarung-only data; the sentiment model is evaluated in-domain (BukuWarung, Experiment A) and cross-app (BukuWarung → KasirPintar, Experiment B); topic modeling is restricted to BukuWarung. Cross-app ROC-AUC (0.95) indicates the model captures language patterns that generalize beyond BukuWarung's vocabulary, though precision for the negative class drops to 48.7% on KasirPintar due to its low base rate (6.9% negative) — see Section 8.

## 2. Sampling window and temporal variation

- Date range: BukuWarung 2022-08-29 to 2026-09-23; KasirPintar 2023-06-09 to 2026-09-23. Both cover multi-year windows of comparable length.
- BukuWarung is persistently negative: about 52.7% negative before Oct 2025 (1,324 of 2,510 labeled reviews) and 54.6% over the last 12 months (443 of 811). The earlier figure is derived by subtracting the last 12 months from the totals.
- BukuWarung's monthly negative share is volatile (8.8% in Nov 2025 up to 89.7% in Mar 2026). Review volume roughly doubled in Jan-Feb 2026 during a complaint wave (63-77% negative), and Nov 2025 shows a positive spike (124 positive vs 12 negative) that may reflect non-organic review activity (hypothesis, not verified).
- KasirPintar stays low-negative in every one of the last 12 months (0%-14.3%).
- Consequence: the gap between the apps is persistent rather than a sampling artifact, but its cause cannot be determined from this data.

## 3. Small negative sample for KasirPintar

Only 177 negative reviews. Per-app keyword analysis and topic modeling for KasirPintar were skipped because results would be dominated by noise. Per-app metrics for this class carry wide uncertainty.

## 4. Review length differs by sentiment

Negative reviews are longer (mean 14.20 vs 7.82 words; median 11 vs 5). Positive reviews are often short and generic, which may make them easier to separate from negative ones.

## 5. Star rating as a sentiment proxy

- Rating 3 reviews (467) were excluded from the classifier. Manual inspection showed several 3-star reviews are clear complaints, so some genuine negative signal is discarded.
- Some low-rating reviews contain clearly positive text. Example (KasirPintar, rating 2): "Sangat membantu usaha saya,terimakasih👍🙏🏻". Example (KasirPintar, rating 1): "mudah di gunakan sangat membantu untuk kami pemula". These are labeled "negatif" by the rating rule despite positive wording — see Section 8 for how this affected an earlier version of the model.

## 6. Self-selection

Play Store reviews come from users who chose to write one and may over-represent extreme experiences.

## 7. Scope of conclusions

Because about 91% of negative reviews come from BukuWarung and KasirPintar has only 177 negative reviews, the pain-point findings describe BukuWarung. They should not be generalized to KasirPintar or to MSME apps as a whole without additional data.

## 8. Issues found and fixed during modeling (Step 5)

Three issues were found while building the sentiment model and keyword analysis, after the pipeline was already producing plausible-looking output. Recorded here because each one could have silently produced misleading conclusions.

**8.1 Negation-stripping bug in preprocessing (Step 3).** The original `Sastrawi.StopWordRemover` occasionally dropped the word adjacent to a removed stopword, including the negation word "tidak" itself in some sentences (e.g. "tetap tidak bisa" → "tetap bisa"). This silently inverted the meaning of affected reviews. Found by comparing word counts in raw vs. cleaned text (`src/check_preprocessing.py`) after noticing "tidak"/"bisa" counts dropped between two runs with no code change to explain it. Fixed by replacing the library's remover with a deterministic stopword filter (`src/id_stopwords.py`) that explicitly protects negation words. After the fix, "tidak" became the single strongest predictor of negative sentiment in the model (coefficient 5.88, more than 1.5x the next strongest feature) — indicating the original bug was suppressing a substantial amount of real signal.

**8.2 Cross-clause bigram contamination.** `CountVectorizer` builds n-grams from the token stream after removing stopwords and ignoring punctuation, so words from unrelated clauses could be paired (e.g. "bagus, tapi sering error" → bigram "bagus sering" after "tapi" is dropped). Fixed by having `src/preprocessing.py` retain clause boundaries (split on `. , ! ? ;`) in a separate `content_clauses` column, and generating bigrams only within a clause (`src/keyword_analysis.py`). Unigram counts and the sentiment/topic models, which don't depend on cross-word adjacency in the same way, were left on the flat `content_clean` column.

**8.3 Sample-weighting amplified label noise.** An earlier version of the final sentiment model used per-(app, label) sample weights to correct for the app imbalance in Section 1. Because KasirPintar's negative class is only 177 reviews, this gave each of those reviews roughly 7x the weight of a BukuWarung negative review. Two mislabeled reviews in that small set (positive text, low rating — see Section 5) were consequently able to push clearly positive phrases ("usaha terimakasih", "membantu pemula") into the model's list of top negative predictors. Found by manually reading the source reviews for the top coefficients (`src/inspect_phrase.py`) instead of taking the coefficient ranking at face value. Fixed by dropping the custom per-cell weighting in favor of plain `class_weight="balanced"`; Experiments A and B (which use simpler within/cross-app splits, not this weighting) were not affected and required no changes.
