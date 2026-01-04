# src/model_trainer.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_and_save(df, target_col, model_path):
    """
    Melatih model dan menyimpan Model + Nama Kolom.
    """
    # 1. Tentukan Fitur
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Latih Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("🤖 Model Random Forest berhasil dilatih.")
    
    # 4. Evaluasi
    score = model.score(X_test, y_test)
    print(f"📊 Akurasi Model (R^2): {score:.2f}")
    
    # 5. SIMPAN PAKET LENGKAP (Model + List Nama Kolom)
    # Ini trik MLOps biar saat deploy urutan kolomnya gak ketuker
    model_package = {
        'model': model,
        'features': X.columns.tolist()
    }
    
    joblib.dump(model_package, model_path)
    print(f"💾 Model & Metadata disimpan di: {model_path}")