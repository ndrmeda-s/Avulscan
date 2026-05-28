from fpdf import FPDF

def generate_pdf_report(target_host, port_data, header_data, output_path):
    """
    Fungsi Enterprise untuk membuat laporan audit keamanan siber.
    Dilengkapi dengan kamus deskripsi port informatif dan diagram batang geometris.
    """
    pdf = FPDF()
    pdf.add_page()

    # ==============================================================================
    # DATABASE DESKRIPSI PORT INFORMASI (Rincian Detail)
    # ==============================================================================
    port_knowledge = {
        21: "FTP (File Transfer Protocol) - Protokol lama untuk transfer file. Jika status OPEN tanpa enkripsi tambahan (FTPS), data kredensial user dikirim dalam bentuk plain-text yang sangat rawan diendus (sniffing) di jaringan.",
        22: "SSH (Secure Shell) - Jalur komunikasi terenkripsi untuk manajemen remote server. Status OPEN adalah wajar untuk admin, namun wajib dilindungi dari serangan Brute-Force dengan mematikan login password dan beralih ke SSH Key.",
        80: "HTTP (Hypertext Transfer Protocol) - Jalur komunikasi web standar tanpa enkripsi. Jika status OPEN, pastikan server otomatis melakukan pengalihan (Redirection) ke jalur aman Port 443 agar user terhindar dari Man-in-the-Middle (MitM) attack.",
        443: "HTTPS (HTTP Secure) - Standar wajib web modern terenkripsi SSL/TLS. Melindungi integritas dan kerahasiaan data pengguna dari intersepsi pihak ketiga selama proses berselancar."
    }

    # ==============================================================================
    # DATABASE DESKRIPSI HTTP SECURITY HEADERS (Rincian Detail)
    # ==============================================================================
    header_knowledge = {
        "Strict-Transport-Security": {
            "secure": "Secure: Memaksa browser menggunakan HTTPS enkripsi ketat. Melindungi pengguna dari pembajakan enkripsi di jaringan publik.",
            "missing": "Vulnerable: Risiko Downgrade Attack. Penyerang dapat memaksa koneksi turun ke HTTP biasa untuk mengintip data komunikasi."
        },
        "Content-Security-Policy": {
            "secure": "Secure: Membatasi eksekusi skrip luar yang tidak sah. Halaman web terlindungi dari eksekusi kode gelap atau injeksi.",
            "missing": "Vulnerable: Risiko Cross-Site Scripting (XSS). Peretas dapat menyuntikkan skrip jahat untuk mencuri cookie atau session."
        },
        "X-Frame-Options": {
            "secure": "Secure: Melarang website dibingkai (iframe) secara ilegal untuk mencegah penipuan manipulasi klik.",
            "missing": "Vulnerable: Risiko Clickjacking. Peretas dapat menumpuk halaman asli di bawah situs jebakan yang transparan."
        },
        "X-Content-Type-Options": {
            "secure": "Secure: Memaksa browser mematuhi MIME type asli file dan melarang eksekusi file berbahaya yang menyamar.",
            "missing": "Vulnerable: Risiko MIME-sniffing exploits. Browser dapat terkecoh mengeksekusi file berbahaya yang menyamar sebagai gambar."
        }
    }

    # ==============================================================================
    # KALKULASI DATA UNTUK DIAGRAM / STATISTIK
    # ==============================================================================
    total_ports = len(port_data)
    open_ports = sum(1 for status in port_data.values() if status == "OPEN")

    total_headers = len(header_data)
    secure_headers = sum(1 for status in header_data.values() if "PRESENT (Secure)" in status)

    # ==============================================================================
    # 1. HEADER BANNER DOKUMEN (Desain Modern)
    # ==============================================================================
    # Membuat kotak background gelap di bagian atas halaman
    pdf.set_fill_color(30, 41, 59) # Warna Slate Gelap
    pdf.rect(0, 0, 210, 38, "F")

    pdf.set_text_color(255, 255, 255) # Teks Putih
    pdf.set_font("Helvetica", style="B", size=18)
    pdf.ln(5)
    pdf.cell(0, 10, "CYBER SECURITY AUDIT REPORT", align="C", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 5, f"Automated Security Scanner Assessment v1.0", align="C", ln=True)
    pdf.ln(12)

    # Reset warna teks ke hitam untuk isi dokumen
    pdf.set_text_color(0, 0, 0)

    # Metadata Target
    pdf.set_font("Helvetica", style="B", size=11)
    pdf.cell(30, 6, "Target Host")
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 6, f": {target_host}", ln=True)
    pdf.ln(6)

    # ==============================================================================
    # 2. SEKSI DIAGRAM & STATISTIK DATA (Executive Summary)
    # ==============================================================================
    pdf.set_font("Helvetica", style="B", size=13)
    pdf.cell(0, 10, "X. Executive Security Statistics", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Garis pembatas horizontal
    pdf.ln(4)

    # --- DIAGRAM 1: RASIO PORT YANG TERBUKA ---
    pdf.set_font("Helvetica", size=10)
    pdf.cell(55, 8, f"Open Ports Exposure ({open_ports}/{total_ports})")

    # Menggambar Track Abu-abu (Background Bar)
    pdf.set_fill_color(226, 232, 240)
    pdf.rect(70, pdf.get_y() + 1.5, 100, 5, "F")
    # Menggambar Isi Grafik (Warna Indigo jika ada port open)
    if open_ports > 0:
        pdf.set_fill_color(79, 70, 229) # Indigo
        width_port_bar = (open_ports / total_ports) * 100
        pdf.rect(70, pdf.get_y() + 1.5, width_port_bar, 5, "F")
    pdf.ln(8)

    # --- DIAGRAM 2: PERSENTASE HEADER YANG AMAN ---
    pdf.cell(55, 8, f"Secure HTTP Headers ({secure_headers}/{total_headers})")

    # Menggambar Track Abu-abu (Background Bar)
    pdf.set_fill_color(226, 232, 240)
    pdf.rect(70, pdf.get_y() + 1.5, 100, 5, "F")
    # Menggambar Isi Grafik (Warna Hijau Emerald)
    if secure_headers > 0:
        pdf.set_fill_color(16, 185, 129) # Emerald Green
        width_header_bar = (secure_headers / total_headers) * 100
        pdf.rect(70, pdf.get_y() + 1.5, width_header_bar, 5, "F")
    pdf.ln(14)

    # ==============================================================================
    # 3. SEKSI RINCIAN DETAIL PORT SCANNING
    # ==============================================================================
    pdf.set_font("Helvetica", style="B", size=13)
    pdf.cell(0, 10, "1. Network Port Scanning Analysis", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    for port, status in port_data.items():
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.cell(22, 6, f"Port {port}")

        # Pewarnaan teks status biar interaktif
        if status == "OPEN":
            pdf.set_text_color(220, 38, 38) # Merah (Butuh perhatian)
        else:
            pdf.set_text_color(71, 85, 105) # Abu-abu aman

        pdf.cell(30, 6, f"[{status}]", ln=True)
        pdf.set_text_color(0, 0, 0) # Reset hitam

        # Mengambil detail penjelasan port dari database internal di atas
        pdf.set_font("Helvetica", size=9)
        description_text = port_knowledge.get(int(port), "Tidak ada data referensi standar untuk port ini.")
        pdf.multi_cell(0, 5, f"Rincian: {description_text}")
        pdf.ln(3)

    pdf.ln(4)

    # ==============================================================================
    # 4. SEKSI RINCIAN DETAIL HTTP SECURITY HEADERS
    # ==============================================================================
    pdf.set_font("Helvetica", style="B", size=13)
    pdf.cell(0, 10, "2. HTTP Security Headers Analysis", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    for header, status in header_data.items():
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.cell(60, 6, f"{header}")

        # Pewarnaan label status header sekaligus mendeteksi status kondisi
        if "PRESENT" in status:
            pdf.set_text_color(16, 185, 129) # Hijau
            header_state = "secure"
        elif "MISSING" in status:
            pdf.set_text_color(217, 119, 6) # Amber/Kuning
            header_state = "missing"
        else:
            pdf.set_text_color(220, 38, 38) # Merah
            header_state = "missing"

        pdf.cell(0, 6, f": {status}", ln=True)
        pdf.set_text_color(0, 0, 0) # Reset hitam

        # Mengambil detail penjelasan header dari database internal baru
        pdf.set_font("Helvetica", style="I", size=9)
        pdf.set_text_color(80, 80, 80) # Abu-abu untuk teks deskripsi detail
        
        header_info = header_knowledge.get(header, {})
        description_text = header_info.get(header_state, "Tidak ada data referensi standar untuk header ini.")
        
        pdf.multi_cell(0, 5, f"Rincian: {description_text}")
        pdf.set_text_color(0, 0, 0) # Reset hitam kembali
        pdf.ln(3)

    # ==============================================================================
    # CETAK FILE
    # ==============================================================================
    pdf.output(output_path)
    return True
