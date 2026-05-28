from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# Mengimport fungsi-fungsi laboratorium siber yang sudah kita ubah di folder core
from core.scanner import run_port_scan
from core.header_scan import run_header_scan
from core.reporter import generate_pdf_report

app = FastAPI(title="Cyber Security Scanner API")

# Mengaktifkan CORS agar Frontend dari Vercel/Netlify nanti bisa mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mengizinkan semua domain mengakses API pada masa pengembangan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Batasan target laboratorium siber yang sah (Hard Whitelist Security)
ALLOWED_TARGETS = ["scanme.nmap.org", "github.com", "auto-scan-chi.vercel.app", "sayuran.vip"]

@app.get("/")
def home():
    return {"status": "Online", "message": "Welcome to Cyber Security Scanner API"}

@app.get("/api/scan")
def do_security_scan(target: str):
    # Validasi Keamanan: Memastikan target yang diminta user terdaftar di whitelist
    if target not in ALLOWED_TARGETS:
        raise HTTPException(status_code=403, detail="Target domain is not allowed for security reasons.")
    
    # 1. Menjalankan fungsi pemindaian port
    ports_results = run_port_scan(target)
    
    # 2. Menjalankan fungsi analisis header keamanan
    headers_results = run_header_scan(target)
    
    # 3. Menentukan lokasi penyimpanan file PDF hasil scan secara otomatis
    pdf_filename = f"report_{target}.pdf"
    pdf_path = os.path.join(os.path.dirname(__file__), pdf_filename)
    
    # 4. Membuat laporan PDF berdasarkan data riil hasil pemindaian di atas
    generate_pdf_report(target, ports_results, headers_results, pdf_path)
    
    # Mengembalikan respon berformat JSON gabungan ke sistem frontend
    return {
        "target": target,
        "ports_status": ports_results,
        "headers_status": headers_results,
        "pdf_report_url": f"/api/download?filename={pdf_filename}"
    }

@app.get("/api/download")
def download_report(filename: str):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    # Memeriksa apakah file PDF yang diminta beneran ada di server backend
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=filename)
    raise HTTPException(status_code=404, detail="File report tidak ditemukan.")
