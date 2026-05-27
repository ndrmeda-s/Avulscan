FROM python:3.11-slim

# Set lokasi kerja langsung ke folder /app di dalam cloud
WORKDIR /app

# Salin HANYA isi dari folder backend lokal ke folder /app cloud
COPY ./backend /app

# Install dependensi bersih (FastAPI, Uvicorn, FPDF2)
RUN pip install --no-cache-dir -r requirements.txt

# Port wajib untuk Hugging Face Spaces
EXPOSE 7860

# Jalankan uvicorn langsung dari posisi /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
