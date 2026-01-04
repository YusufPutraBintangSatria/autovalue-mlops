# src/data_loader.py
import pandas as pd

def load_data(filepath):
    """Membaca data dari CSV."""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Data berhasil dimuat. Total baris: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"❌ File tidak ditemukan di: {filepath}")
        return None

def clean_data(df):
    """
    Membersihkan data dan Feature Engineering (Extract Model Name).
    """
    # 1. Hapus data kosong
    df = df.dropna()
    
    # --- FEATURE ENGINEERING BARU (PHASE 2.5) ---
    # Kita ambil kata pertama dari 'car name' sebagai Model
    # Contoh: "YARIS S TRD 1.5" -> "YARIS"
    # Pastikan kolom 'car name' ada
    if 'car name' in df.columns:
        df['model'] = df['car name'].apply(lambda x: str(x).split()[0])
    else:
        print("⚠️ Warning: Kolom 'car name' tidak ditemukan!")

    # 2. Filter Kolom Penting (Sekarang tambah 'model')
    # Perhatikan: Kita pakai 'model' hasil ekstrak tadi, bukan 'car name' lagi
    kolom_penting = ['brand', 'model', 'year', 'mileage (km)', 'transmission', 'price (Rp)']
    
    try:
        df = df[kolom_penting]
    except KeyError as e:
        print(f"⚠️ Warning: Ada kolom yang hilang. Error: {e}")

    # 3. One-Hot Encoding
    # Sekarang kita encode juga 'model'-nya
    # dtype=int agar hasilnya angka 0/1 (bukan True/False) -> Menghilangkan Warning
    df = pd.get_dummies(df, columns=['brand', 'model', 'transmission'], dtype=int)
    
    print(f"🧹 Data dibersihkan. Total Fitur sekarang: {len(df.columns)}")
    return df