# Problem Statement: BukuWarung User Pain Points

## Scope

This problem statement is based on 1,767 negative (1-2 star) reviews of **BukuWarung** on the Google Play Store. Findings describe BukuWarung specifically and should **not** be generalized to KasirPintar or to MSME financial apps broadly. 91% of negative reviews in the combined dataset come from BukuWarung; KasirPintar's negative sample (177 reviews) is too small for reliable standalone analysis. See `data-limitations.md` for the full discussion.

## Methodology

Pain points were identified through two independent methods, cross-validated against each other:

1. **Bigram distinctiveness analysis** (`keyword_analysis.py`) — phrases disproportionately common in negative vs. positive reviews, with clause-boundary-aware bigram extraction to avoid false phrase pairings.
2. **Topic modeling via LDA** (`topic_modeling.py`) — thematic clustering of negative reviews.

Both methods converged on the same five themes (see `topic-modeling-results.md`). Prevalence for each theme was then measured directly by keyword/phrase matching against all 1,767 negative reviews (`problem_statement_helper.py`). Keyword choices for each theme were checked against sampled example quotes and revised twice after manual review surfaced false matches (see Section 8 of `data-limitations.md` for the sentiment-model debugging process, and the commit history of `problem_statement_helper.py` for this document's own keyword corrections).

A review can touch more than one theme, so the percentages below do not sum to 100%.

## Ranked Pain Points

### 1. Saldo / QRIS / verification issues — 305 reviews (17.3%)

Users report payments not reflecting in their balance, failed top-ups, and friction registering for QRIS (requiring an in-person sales visit to get a registration code).

> "3x transaksi yg gak masuk ke rekening saya sejak tanggal 5 des kemarin... pelanggan membayar tertera berhasil dan langsung kepotong saldonya. kenapa dananya gak masuk di rekening saya?" — rating 1

> "kita daftar qris.. harus ada sales yg datang dan ngasih kode sales.. mana mungkin di cc" — rating 1

### 2. Slow customer service response — 193 reviews (10.9%)

Users describe CS as unresponsive, bot-like, or slow to resolve issues — often raised while trying to report one of the other problems in this list.

> "chat cs sumpah gak ada nyambung nya selalu bales bot" — rating 1

> "Respon CS tlong agak cepat dong Lelet banget, Bkn ny slesai malah ngulang lg laporan ny" — rating 2

### 3. UI/navigation: the "0" button is unreachable — 149 reviews (8.4%)

A specific, reproducible bug: the bottom navigation bar overlaps the "0" digit button on the numeric keypad, making certain amounts impossible to enter. Of the five pain points, this is the one with the **single clearest, most isolated root cause** — a layout regression, not a diffuse or backend-dependent issue.

> "gak bisa pencet tombol 0" — rating 1

> "tombol nol nya jadi ketutupan tombol navigasi.. kalau kelamaan gini auto pindah aplikasi lain" — rating 1

### 4. App crashes / force-closes — 90 reviews (5.1%)

> "habis update malah keluar2 terus bagaimana solusinya payah banget" — rating 2

> "Tolong diperbaiki bug force close apabila kita update data yang di cadangkan" — rating 1

### 5. Data/records lost — 89 reviews (5.0%)

> "Bertahun tahun pakai ni aplikasi sudah baru kali ini aplikasi erornya laaammaa, data2 pelanggan hilang semua, saldo dalam aplikasi kemanaa" — rating 2

> "Akun tiba2 sign out.. mau sign in ga bisa padahal otp dah bener.. data2 penting hilang semua.. jd harus input ulang" — rating 1

**Note:** in 2 of the 3 sampled quotes for this theme, data loss is described as following an unexpected crash or forced logout — the same failure mode as Pain Point #4. This suggests the two may share a root cause rather than being fully independent problems; worth investigating together if addressed in a prototype.

## Cross-cutting observation: issues cluster around app updates

263 reviews (14.9%) mention "update" in connection with a negative experience — spanning several different root causes (UI regressions, slower performance, new bugs) rather than one single issue, so it is reported here separately rather than as a sixth pain point.

> "sering banget setelah update malah lebih lelet" — rating 1

> "Kenapa setelah di update mkn ribet n susah" — rating 1

This lines up with a temporal pattern found during exploratory analysis (`data_diagnostics.py`): BukuWarung's monthly negative-review share jumped from 8.8% (Nov 2025) to 63-89% (Jan-Mar 2026). The specific app version responsible was not identified — this is a plausible explanation for the spike, not a verified one.

## Coverage

708 of 1,767 negative reviews (40.1%) matched at least one of the five pain points above. The remaining ~60% are complaints outside these categories — reviews too vague to categorize ("jelek", "aplikasi sampah"), or feedback about pricing/business model/feature requests rather than bugs.

## Implications for MVP scope (Step 7)

Saldo/QRIS/verification issues are the most frequent and touch the core trust proposition of a financial app, but very likely involve backend or third-party payment infrastructure outside the reach of a lightweight student prototype. The UI/navigation bug (#3) is the most tractable to demonstrate: it has a single, well-defined, reproducible cause, requires no backend, and directly illustrates the project's research-to-prototype pipeline. Candidate framing for Step 7: a corrected numeric-entry UI component, positioned as a fix for the specific, evidenced bug described above.
