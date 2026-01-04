# 🚗 AutoValue Pro: MLOps Car Valuation System

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Model-Random%20Forest-orange?style=for-the-badge&logo=scikit-learn)
![Docker](https://img.shields.io/badge/Deployment-Docker-blue?style=for-the-badge&logo=docker)

**AutoValue Pro** adalah sistem prediksi harga mobil bekas berbasis Machine Learning yang dibangun dengan prinsip **MLOps (Machine Learning Operations)**. Proyek ini bukan sekadar model prediksi, melainkan aplikasi *End-to-End* yang mencakup Data Pipeline, Model Training, dan Deployment Interface.

---

## 🌟 Fitur Utama
* **Smart Preprocessing:** Menggunakan pipeline otomatis untuk pembersihan data dan *One-Hot Encoding*.
* **Advanced Modeling:** Menggunakan algoritma **Random Forest Regressor** yang mampu menangkap pola non-linear harga mobil.
* **Dynamic UI:** Antarmuka web interaktif dengan *Linked Dropdown* (Pilihan Model menyesuaikan Brand).
* **Modular Architecture:** Kode terstruktur rapi (`src/`, `data/`, `models/`) memudahkan maintenance dan skalabilitas.
* **Dockerized:** Siap di-deploy di mana saja menggunakan Container.

## 📂 Struktur Proyek
```text
project-autovalue/
├── data/               # Penyimpanan Data Mentah & Proses
├── models/             # Artifact Model (.pkl)
├── src/                # Source Code Modular (Loader, Trainer)
├── app/                # Aplikasi Frontend (Streamlit)
├── Dockerfile          # Konfigurasi Container
└── requirements.txt    # Daftar Dependensi