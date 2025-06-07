# Dockerfile

# 1. Gunakan base image Python yang ringan
FROM python:3.9

# 2. Set direktori kerja di dalam kontainer
WORKDIR /app

# 3. Copy file requirements dan install dependencies terlebih dahulu
#    Ini akan memanfaatkan cache Docker jika requirements tidak berubah
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy sisa kode aplikasi ke dalam kontainer
COPY . .

# 5. Jalankan aplikasi menggunakan Uvicorn saat kontainer start
#    --host 0.0.0.0 penting agar bisa diakses dari luar kontainer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]