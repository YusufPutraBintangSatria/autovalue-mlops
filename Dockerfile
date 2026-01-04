# 1. Base Image: Kita pakai "Laptop Virtual" yang sudah ada Python 3.9 versi ringan (slim)
FROM python:3.9-slim

# 2. Work Directory: Bikin folder kerja di dalam laptop virtual itu
WORKDIR /app

# 3. Copy Resep Library: Masukkan requirements.txt dari laptop asli ke laptop virtual
COPY requirements.txt .

# 4. Install Library: Suruh laptop virtual install semua bahan
# Kita tambah --no-cache-dir biar ukuran kotaknya kecil
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Kode: Masukkan semua folder (src, app, data, models) ke laptop virtual
COPY . .

# 6. Expose Port: Buka pintu nomor 8501 (Pintu standar Streamlit)
EXPOSE 8501

# 7. Command: Perintah yang otomatis jalan saat kotak dibuka
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]