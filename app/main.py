import streamlit as st
import pandas as pd
import joblib

# 1. LOAD MODEL & DATA
@st.cache_resource
def load_resources():
    package = joblib.load('models/model_v1.pkl')
    df = pd.read_csv('data/raw/car_price.csv')
    df['model_clean'] = df['car name'].apply(lambda x: str(x).split()[0])
    return package['model'], package['features'], df

try:
    model, model_features, df_cars = load_resources()
except FileNotFoundError:
    st.error("File sistem hilang. Silakan hubungi admin.")
    st.stop()

# 2. HEADER
st.title("🚗 AutoValue Pro: Smart AI Valuation")
st.write("Sistem estimasi harga mobil bekas berbasis data historis.")

# 3. SIDEBAR (Input User)
st.sidebar.header("Spesifikasi Mobil")

# --- A. BRAND & MODEL (Linked Dropdown) ---
list_brand = sorted(df_cars['brand'].unique().tolist())
brand = st.sidebar.selectbox("Merek", list_brand)

list_model = sorted(df_cars[df_cars['brand'] == brand]['model_clean'].unique().tolist())
car_model = st.sidebar.selectbox("Model", list_model)

# Filter Dataframe berdasarkan Brand & Model terpilih
data_mobil_ini = df_cars[
    (df_cars['brand'] == brand) & 
    (df_cars['model_clean'] == car_model)
]

# --- B. TRANSMISI DINAMIS ---
# Cek transmisi apa saja yang tersedia untuk mobil ini di database
available_trans = sorted(data_mobil_ini['transmission'].unique().tolist())
transmission = st.sidebar.radio("Transmisi", available_trans)

# --- C. TAHUN (Dengan Info Range) ---
min_year = int(data_mobil_ini['year'].min())
max_year = int(data_mobil_ini['year'].max())
st.sidebar.caption(f"📅 Data tersedia: {min_year} - {max_year}")

year = st.sidebar.slider("Tahun Pembuatan", 2000, 2025, 2018)

# --- D. KILOMETER (Dengan Statistik) ---
avg_km = int(data_mobil_ini['mileage (km)'].mean())
max_km_db = int(data_mobil_ini['mileage (km)'].max())

mileage = st.sidebar.number_input("Kilometer (KM)", min_value=0, value=avg_km, step=1000)
st.sidebar.caption(f"Rata-rata KM model ini: {avg_km:,} km")

# 4. LOGIKA PREDIKSI & VALIDASI
if st.button("🔍 Cek Estimasi Harga"):
    
    # --- VALIDASI (Guardrails) ---
    errors = []
    warnings = []

    # 1. Cek Tahun
    if year > max_year:
        errors.append(f"⚠️ Data {brand} {car_model} tahun {year} belum tersedia (Maks: {max_year}).")
    elif year < min_year:
        errors.append(f"⚠️ Data {brand} {car_model} tahun {year} terlalu tua (Min: {min_year}).")

    # 2. Cek Kilometer (Soft Warning)
    if mileage > max_km_db + 50000:
        warnings.append(f"⚠️ KM {mileage:,} tergolong sangat tinggi. Akurasi mungkin berkurang.")
    elif mileage < 1000:
        warnings.append("⚠️ KM terlalu rendah (Hampir baru). Pastikan input benar.")

    # --- KEPUTUSAN ---
    if errors:
        for e in errors:
            st.error(e)
        st.info("Sistem menolak prediksi untuk menjaga kualitas data.")
    else:
        # Tampilkan Warning kalau ada (tapi tetap lanjut prediksi)
        for w in warnings:
            st.warning(w)

        # PREDIKSI
        input_data = {col: 0 for col in model_features}
        input_data['year'] = year
        input_data['mileage (km)'] = mileage
        
        # One-Hot Encoding Manual
        input_data[f"brand_{brand}"] = 1
        input_data[f"model_{car_model}"] = 1
        input_data[f"transmission_{transmission}"] = 1
        
        # Eksekusi Model
        df_input = pd.DataFrame([input_data])
        try:
            prediction = model.predict(df_input)[0]
            st.success(f"💰 Estimasi Harga: Rp {int(prediction):,}")
            
            # Analisis Tambahan
            avg_price = data_mobil_ini['price (Rp)'].mean()
            diff = prediction - avg_price
            status = "Di Atas Rata-rata" if diff > 0 else "Di Bawah Rata-rata"
            color = "red" if diff > 0 else "green"
            
            st.markdown(f"**Analisis Pasar:** Harga ini : **{status}** pasar.")
            
        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {e}")