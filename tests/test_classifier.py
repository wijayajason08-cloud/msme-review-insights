import os
import sys

# Supaya bisa import modul dari folder src/ saat pytest dijalankan dari root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from feedback_classifier import analyze_feedback, detect_categories, predict_sentiment


def test_predict_sentiment_negative():
    label, confidence = predict_sentiment(
        "aplikasi jelek sekali, saldo saya hilang, sangat kecewa"
    )
    assert label == "negatif"
    assert confidence > 0.5


def test_predict_sentiment_positive():
    label, confidence = predict_sentiment(
        "aplikasi sangat membantu usaha saya, mudah digunakan, mantap"
    )
    assert label == "positif"
    assert confidence > 0.5


def test_detect_categories_match_saldo():
    categories = detect_categories("saldo saya tidak masuk setelah transaksi qris")
    assert "Saldo/QRIS/verifikasi bermasalah" in categories


def test_detect_categories_match_multiple():
    categories = detect_categories("aplikasi keluar sendiri terus, lalu data hilang semua")
    assert "Aplikasi keluar sendiri / crash" in categories
    assert "Data/catatan hilang" in categories


def test_detect_categories_no_match():
    categories = detect_categories("aplikasi bagus sekali, terima kasih")
    assert categories == []


def test_analyze_feedback_empty_text():
    result = analyze_feedback("")
    assert "error" in result


def test_analyze_feedback_full_result():
    result = analyze_feedback("tombol angka 0 tertutup navigasi, susah input")
    assert result["sentiment"] == "negatif"
    assert "UI/navigasi: tombol & angka 0 tidak bisa diketik" in result["categories"]