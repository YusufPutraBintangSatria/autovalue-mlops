# ARCHITECTURE DOCUMENT: AutoValue Pro (AI Car Valuation System)

**Project Status:** 🚧 Planning Phase
**Version:** 1.0.0
**Owner:** Bintang (MLOps Engineer)
**Goal:** Mengubah script prediksi harga sederhana menjadi aplikasi Enterprise-ready yang scalable, modular, dan ter-deploy secara profesional.

---

## 1. High-Level Overview
Aplikasi ini bukan sekadar kalkulator harga. Ini adalah sistem "End-to-End MLOps" yang memisahkan antara:
1.  **Data Pipeline:** Pengolahan data mentah.
2.  **Model Training:** Pelatihan model AI.
3.  **Inference Engine:** API yang melayani prediksi.
4.  **User Interface:** Tampilan web untuk user.

---

## 2. Tech Stack (Standard MLOps)
* **Language:** Python 3.9+
* **Version Control:** Git & GitHub
* **Environment:** `venv` (Virtual Environment)
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn, XGBoost (Upgrade dari Linear Regression nanti)
* **Frontend:** Streamlit
* **Backend/API (Future):** FastAPI (Untuk memisahkan otak AI dari tampilan)
* **Containerization:** Docker (Agar jalan di server manapun)
* **Experiment Tracking:** MLflow (Untuk mencatat performa model)

---

## 3. Directory Structure (Struktur Folder Baku)
Jangan campur semua file di luar. Ikuti struktur ini:

```text
project-autovalue/
├── .gitignore               # Daftar file yang diabaikan Git (Data, venv, secrets)
├── architecture.md          # DOKUMEN INI (Peta Utama)
├── README.md                # Penjelasan singkat cara install untuk orang lain
├── requirements.txt         # Daftar library & versi (Frozen)
│
├── data/                    # TEMPAT PENYIMPANAN DATA (Di-ignore Git)
│   ├── raw/                 # Data mentah (CSV asli)
│   ├── processed/           # Data bersih siap training
│   └── external/            # Data tambahan (jika ada)
│
├── models/                  # TEMPAT MENYIMPAN OTAK AI
│   ├── model_v1.pkl         # Model regresi v1
│   └── scaler.pkl           # Penyimpan logika scaling/normalisasi
│
├── notebooks/               # TEMPAT CORET-CORETAN (Eksperimen)
│   ├── 01_eda.ipynb         # Analisis data awal
│   └── 02_training.ipynb    # Coba-coba algoritma
│
├── src/                     # SOURCE CODE UTAMA (Modular)
│   ├── __init__.py
│   ├── data_loader.py       # Script khusus baca & bersihkan data
│   ├── model_trainer.py     # Script khusus melatih & simpan model
│   └── predictor.py         # Script khusus memanggil model (Inference)
│
└── app/                     # FRONTEND (Tampilan Web)
    ├── main.py              # File utama Streamlit
    └── utils.py             # Fungsi bantuan untuk UI