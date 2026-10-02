# MVP Scope: Feedback Sentiment & Pain-Point Classifier

## Problem Being Addressed

Business owners and support teams receive free-text feedback (app reviews, support chats, surveys) with no star rating attached, making it hard to quickly tell which messages are urgent complaints and what they're about. This MVP demonstrates a lightweight tool that automatically classifies incoming feedback by sentiment and pain-point category, using the models and categories already validated in this project.

## Alternatives Considered

| Option | Verdict |
|---|---|
| Fix the UI/navigation bug (Pain Point #3) | Rejected. Technically the simplest and has the clearest root cause, but unrelated to the NLP work done in Steps 5-6 — would not demonstrate AI engineering skills, and wastes the trained model. |
| Fix Saldo/QRIS issues (Pain Point #1, most frequent) | Rejected. Very likely requires backend or third-party payment infrastructure, out of reach for a lightweight student prototype. |
| **Feedback Classifier Tool (chosen)** | Directly reuses the trained sentiment model (ROC-AUC 0.92 in-domain, 0.95 cross-app — see `sentiment_model.py` results) and the five validated pain-point categories from `problem-statement.md`. Turns the research output into something usable rather than a one-off analysis. |

## Core Features (max 4)

1. **Text input** — paste or type a piece of feedback/review text.
2. **Sentiment prediction** — positif/negatif classification with a confidence score, using `models/sentiment_model.pkl` and `models/tfidf_vectorizer.pkl`.
3. **Pain-point category detection** — flags which of the 5 validated categories (Saldo/QRIS, CS response, UI/navigation, Crash, Data loss) the text matches, reusing the keyword logic from `problem_statement_helper.py`. A text can match zero, one, or several categories.
4. **Session history table** — a running log of analyzed entries (text, sentiment, categories) shown below the input, so multiple pieces of feedback can be reviewed at a glance.

## User Flow

1. User opens the app.
2. User pastes or types feedback text into a text box.
3. User clicks "Analisis".
4. App displays: sentiment label + confidence, and any matched pain-point category tags.
5. The entry is appended to the history table below.
6. User repeats with new text as needed.

## Out of Scope for This MVP

- Persistent storage across sessions (history is kept in memory only, cleared on refresh).
- A trained multi-label classifier for category detection — keyword-based for now. Noted as a future improvement, not required for the MVP.
- Any fix to the UI/navigation bug itself (a separate, unrelated problem — see "Alternatives Considered").
- Authentication or multi-user support.

## Definition of Done

- App runs locally via `streamlit run src/app.py` without errors.
- Pasting a known negative review (e.g., a quote from `problem-statement.md`) correctly predicts "negatif" and flags the expected category.
- Pasting a clearly positive text predicts "positif" with no category flags.
