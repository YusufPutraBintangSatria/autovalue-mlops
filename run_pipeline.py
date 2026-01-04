# run_pipeline.py
from src.data_loader import load_data, clean_data
from src.model_trainer import train_and_save

# KONFIGURASI
DATA_PATH = "data/raw/car_price.csv"
MODEL_OUTPUT = "models/model_v1.pkl"
TARGET = 'price (Rp)' # Nama kolom target harga

def main():
    print("🚀 Memulai ML Pipeline Phase 2 (Upgrade)...")
    
    # 1. Load
    df = load_data(DATA_PATH)
    
    if df is not None:
        # 2. Clean & Encode (Teks jadi Angka)
        df_clean = clean_data(df)
        
        # 3. Train
        train_and_save(df_clean, TARGET, MODEL_OUTPUT)
        
        print("✅ Pipeline Phase 2 Selesai!")

if __name__ == "__main__":
    main()