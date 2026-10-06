import os
import sys

# Jaga-jaga agar import sibling module (feedback_classifier, dkk) selalu
# berhasil terlepas dari cara Streamlit menjalankan skrip ini.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import streamlit as st

from feedback_classifier import analyze_feedback

st.set_page_config(page_title="Feedback Classifier - BukuWarung", page_icon="📊")

st.title("📊 Feedback Sentiment & Pain-Point Classifier")
st.caption(
    "Analisis otomatis sentimen dan kategori keluhan dari feedback/review BukuWarung. "
    "Dibangun dari model dan kategori yang divalidasi di docs/problem-statement.md."
)

if "history" not in st.session_state:
    st.session_state.history = []

text_input = st.text_area(
    "Masukkan teks feedback/review:",
    height=100,
    placeholder="Contoh: Aplikasi sering force close setelah update...",
)

if st.button("Analisis", type="primary"):
    result = analyze_feedback(text_input)

    if "error" in result:
        st.warning(result["error"])
    else:
        col1, col2 = st.columns(2)
        with col1:
            if result["sentiment"] == "negatif":
                st.error(f"Sentimen: **{result['sentiment'].upper()}**")
            else:
                st.success(f"Sentimen: **{result['sentiment'].upper()}**")
        with col2:
            st.metric("Confidence", f"{result['confidence'] * 100:.1f}%")

        if result["categories"]:
            st.write("**Kategori pain point terdeteksi:**")
            st.markdown(" ".join(f"`{cat}`" for cat in result["categories"]))
        else:
            st.write("Tidak ada kategori pain point spesifik terdeteksi.")

        st.session_state.history.append(
            {
                "Teks": text_input[:80] + ("..." if len(text_input) > 80 else ""),
                "Sentimen": result["sentiment"],
                "Confidence": f"{result['confidence'] * 100:.1f}%",
                "Kategori": ", ".join(result["categories"]) if result["categories"] else "-",
            }
        )

st.divider()
st.subheader("Riwayat Analisis (sesi ini)")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
else:
    st.write("Belum ada feedback yang dianalisis.")