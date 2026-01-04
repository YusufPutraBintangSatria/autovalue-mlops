import streamlit as st
import pandas as pd
import joblib

# 1. LOAD MODEL & DATA UNTUK MENU
@st.cache_resource
def load_resources():
    # Load Model
    package = joblib.load('models/model_v1.pkl')
    
    # Load Data Asli (Hanya untuk ambil daftar Merek & Model yang valid)
    df = pd.read_csv('data/raw/car_price.csv')
    
    # Bersihkan nama model (Sama seperti logika di Training)
    # Ambil kata pertama dari 'car name' (Misal: "INNOVA G DIESEL" -> "INNOVA")
    df['model_clean'] = df['car name'].apply(lambda x: str(x).split()[0])
    
    return package['model'], package['features'], df

try:
    model, model_features, df_cars = load_resources()
except FileNotFoundError:
    st.error("File tidak ditemukan! Pastikan 'models/model_v1.pkl' dan 'data/raw/car_price.csv' ada.")
    st.stop()

# 2. JUDUL WEB
st.title("🚗 AutoValue Pro: AI Car Valuation")
st.write("Prediksi harga mobil bekasmu dengan kekuatan Machine Learning.")

# 3. FORM INPUT USER (Side Bar)
st.sidebar.header("Informasi Mobil")

# --- LOGIKA DROPDOWN PINTAR (LINKED LIST) ---

# A. Ambil daftar Brand unik dari CSV, lalu urutkan abjad
list_brand = sorted(df_cars['brand'].unique().tolist())
brand = st.sidebar.selectbox("Merek (Brand)", list_brand)

# B. Filter Model berdasarkan Brand yang dipilih di atas 👆
# "Ambil semua model_clean, TAPI hanya yang brand-nya == brand yang dipilih user"
list_model = sorted(df_cars[df_cars['brand'] == brand]['model_clean'].unique().tolist())
car_model = st.sidebar.selectbox("Model Mobil", list_model)

# C. Input Lainnya
year = st.sidebar.slider("Tahun Pembuatan", 2000, 2025, 2018)
mileage = st.sidebar.number_input("Kilometer (KM)", min_value=0, value=50000)
transmission = st.sidebar.radio("Transmisi", ['Automatic', 'Manual'])

# 4. LOGIKA PREDIKSI (Tombol)
if st.button("🔍 Cek Harga Pasar"):
    # Siapkan data kosong
    input_data = {col: 0 for col in model_features}
    
    # Isi data numerik
    input_data['year'] = year
    input_data['mileage (km)'] = mileage
    
    # Isi One-Hot Encoding
    brand_col = f"brand_{brand}"
    model_col = f"model_{car_model}"
    trans_col = f"transmission_{transmission}"
    
    # Debugging: Cek apakah kolom ini dikenali model?
    missed_cols = []
    
    if brand_col in input_data:
        input_data[brand_col] = 1
    else:
        missed_cols.append(brand_col)
        
    if model_col in input_data:
        input_data[model_col] = 1
    else:
        missed_cols.append(model_col)
        
    if trans_col in input_data:
        input_data[trans_col] = 1
        
    # Ubah ke DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Prediksi
    prediction = model.predict(df_input)[0]
    
    # Tampilkan Hasil
    st.success(f"💰 Estimasi Harga: Rp {int(prediction):,}")
    
    if prediction < 100000000:
        st.info("💡 Tips: Mobil ini tergolong ekonomis (< 100 Juta).")
    elif prediction > 500000000:
        st.warning("🔥 Wow: Ini termasuk mobil kelas atas!")

    # Pesan Error halus jika ada data baru yang belum pernah dipelajari AI
    if missed_cols:
        st.warning(f"⚠️ Catatan: Model AI belum pernah melihat mobil jenis '{car_model}' sebelumnya, jadi prediksinya mungkin kurang akurat.")