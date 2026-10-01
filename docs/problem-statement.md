# Problem Statement

## Scope

This problem statement describes pain points found in negative (1-2 star) user reviews of **BukuWarung** on the Google Play Store. Findings should **not** be generalized to KasirPintar or to MSME apps in general. BukuWarung accounts for ~91% of all negative reviews in the combined dataset, and KasirPintar has only 177 negative reviews — too few to support its own reliable findings. See `data-limitations.md` (Section 7) for details.

## Methodology

1. Scraped ~4,000 reviews each from BukuWarung and KasirPintar on the Play Store
2. Cleaned and preprocessed text (Indonesian stopword removal that explicitly preserves negation words; slang normalization)
3. Scored distinctive negative-review language using proportion-based comparison against positive reviews (unigrams, and clause-aware bigrams that don't cross comma/period boundaries)
4. Trained a sentiment classifier (TF-IDF + Logistic Regression), validated both within BukuWarung and cross-app (BukuWarung → KasirPintar)
5. Ran topic modeling (LDA) on BukuWarung negative reviews; cross-validated the resulting topics against the bigram findings from step 3 (see `topic-modeling-results.md`)
6. Quantified each resulting pain point's prevalence across all 1,767 negative BukuWarung reviews via keyword/phrase matching, with real review quotes pulled as evidence (`src/problem_statement_helper.py`)

**Note on the numbers below:** percentages do not sum to 100%, since a single review can touch on more than one pain point. Only 40.1% of negative reviews matched at least one of the five categories below — the rest are typically brief, non-specific complaints ("jelek", "buruk", single-word ratings) or issues too rare/varied to form a distinct, evidenced category.

## Pain Points (ranked by prevalence)

### 1. Saldo, QRIS, and account verification problems — 17.3% (305 of 1,767 reviews)

Users report payments or top-ups not reflecting in their balance, slow or unresolved support responses for these payment issues, and friction in the QRIS registration process (requiring an in-person sales agent visit to register).

> "3x transaksi yg gak masuk ke rekening saya sejak tanggal 5 des kemarin... pelanggan membayar tertera berhasil dan langsung kepotong saldonya, kenapa dananya gak masuk di rekening saya?" — rating 1
> *("3 transactions haven't reached my account since Dec 5... the customer paid, it shows as successful, and the balance was deducted immediately — why hasn't the money reached my account?")*

> "Top up saldo bisa sekali mau transaksi tidak bisa... cepat balikan saldo saya" — rating 1
> *("I could top up once, but the transaction won't go through... refund my balance quickly")*

This is the single most common pain point, and the highest-stakes one — it involves the user's actual money, not just app inconvenience.

### 2. Slow or unhelpful customer service — 10.9% (193 of 1,767 reviews)

Users report long response times, bot-like or unhelpful replies in chat support, and issues left unresolved after contacting CS.

> "Respon CS tlong agak cepat dong Lelet banget, Bkn ny slesai malah ngulang lg laporan ny" — rating 2
> *("Please make CS response faster, it's very slow — instead of resolving it, I had to repeat my report")*

This overlaps with Pain Point #1: several saldo/QRIS complaints also mention frustration with CS response time while trying to resolve the payment issue. The two problems likely compound each other rather than being fully independent.

### 3. UI/navigation: input button blocked by navigation bar — 8.4% (149 of 1,767 reviews)

A specific, reproducible UI bug: the on-screen "0" digit button (used to enter transaction amounts) is partially or fully covered by the phone's navigation bar, making it difficult or impossible to tap. Reported across multiple phone brands (Redmi, Xiaomi named explicitly by users).

> "Ini kok jadi tombol nol nya jadi ketutupan tombol navigasi.. kalau kelamaan gini auto pindah aplikasi lain." — rating 1
> *("The 0 button is now covered by the navigation button... if this takes too long it auto-switches to another app")*

> "gak bisa pencet tombol 0" — rating 1
> *("can't tap the 0 button")*

Unlike the other pain points, this is a narrow, well-defined UI layout bug rather than a backend/infrastructure issue — a plausible candidate for a quick, visible fix.

### 4. App crashes or logs out unexpectedly — 5.1% (90 of 1,767 reviews)

Users report the app force-closing or logging them out mid-use, sometimes during a transaction.

> "gimana ini ko aplikasi nya keluar terus data yg punya utang disana semua" — rating 1
> *("why does the app keep closing, all the debt records are in there")*

This may be a contributing cause of Pain Point #5 below — see note there.

### 5. Data/records lost — 5.0% (89 of 1,767 reviews)

Users report customer records, transaction history, or balance data disappearing — in several cases immediately after being signed out unexpectedly.

> "Akun tiba2 sign out.. mau sign in ga bisa padahal otp dah bener.. data2 penting hilang semua.. jd harus input ulang.. bikin repot" — rating 1
> *("Account suddenly signed me out... I can't sign back in even though the OTP was correct... all my important data is gone... I have to re-enter everything, it's a hassle")*

**Hypothesis, not confirmed:** 2 of the 3 manually-read examples in this category explicitly connect data loss to an unexpected sign-out. This category may not be fully independent from Pain Point #4 — data loss could be a downstream consequence of the same crash/logout bug, rather than a separate root cause. This is based on a small manually-read sample (n=3), not a statistically verified causal link.

## Cross-cutting pattern: complaints following app updates — 14.9% (263 of 1,767 reviews)

Reviews mentioning "update" span multiple pain points above rather than forming their own category. Some describe new bugs appearing right after an update. This is plausibly connected to the Jan-Feb 2026 complaint spike independently documented in `data_diagnostics.py` (BukuWarung's negative review share rose to 63-77% in that window, against a baseline closer to 53%). This suggests update releases are a recurring source of regressions, though which specific app version(s) were responsible was not identified from this data.

## What this analysis does NOT establish

- **Causation.** This identifies correlated complaint patterns in review text, not confirmed root causes in the app's code.
- **Generalization beyond BukuWarung.** See `data-limitations.md`, Section 7.
- **Which exact app update(s) caused which bug.** The "update" pattern is suggestive, not confirmed.
- **The Pain Point #4 → #5 causal link.** Plausible from a small reading sample, not independently verified at scale.

See `docs/data-limitations.md` for the full list of data limitations and methodology caveats (including bugs found and fixed during this analysis), and `docs/topic-modeling-results.md` for the topic modeling results this builds on.