import urllib.request
import urllib.error # Kita import library error penanganan HTTP
import ssl

def run_header_scan(target_host):
    """
    Fungsi pemindaian HTTP Security Headers tingkat lanjut.
    Dilengkapi Stealth User-Agent dan kemampuan membaca header pada status HTTP Error.
    """
    security_headers = {
        "Strict-Transport-Security": "Forces HTTPS connections",
        "Content-Security-Policy": "Protects against XSS attacks",
        "X-Frame-Options": "Protects against Clickjacking",
        "X-Content-Type-Options": "Prevents MIME-sniffing exploits"
    }
    header_results = {}
    urls_to_try = [f"https://{target_host}", f"http://{target_host}"]
    unverified_ssl_context = ssl._create_unverified_context()
    
    server_headers = None
    connection_success = False

    for url in urls_to_try:
        try:
            # UPGRADE 1: Menyamar jadi Browser Chrome Windows Asli (Bypass Firewall)
            request_setup = urllib.request.Request(
                url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                }
            )
            with urllib.request.urlopen(request_setup, timeout=4, context=unverified_ssl_context) as response:
                server_headers = response.info()
                connection_success = True
                break 
                
        except urllib.error.HTTPError as e:
            # UPGRADE 2: Jika kena blokir (403/404), TETAP ambil headernya dari objek error!
            print(f"[!] Target merespon dengan HTTP {e.code} pada {url}. Mengekstrak header sisa...")
            server_headers = e.headers
            connection_success = True
            break
            
        except Exception as e:
            # Log kendala koneksi fisik ke terminal Termux untuk debugging
            print(f"[-] Gagal terkoneksi ke {url}. Alasan: {e}")
            continue 

    # ==============================================================================
    # EVALUASI HASIL RESPONS HEADER
    # ==============================================================================
    if connection_success and server_headers is not None:
        for header_name, description in security_headers.items():
            # Memeriksa keberadaan header secara case-insensitive (mengabaikan huruf besar/kecil)
            found_key = None
            for k in server_headers.keys():
                if k.lower() == header_name.lower():
                    found_key = k
                    break
            
            if found_key:
                header_results[header_name] = "PRESENT (Secure)"
            else:
                header_results[header_name] = f"MISSING (Vulnerable - {description})"
    else:
        for header_name, description in security_headers.items():
            header_results[header_name] = "ERROR (Could not analyze)"
            
    return header_results
