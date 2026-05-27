import socket

def run_port_scan(target_host):
    """
    Fungsi inti pemindaian port jaringan.
    Menerima parameter string host target dan mengembalikan hasil dalam bentuk dictionary.
    """
    ports_to_scan = [21, 22, 80, 443]
    scan_results = {}
    
    for port in ports_to_scan:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        connection_status = s.connect_ex((target_host, port))
        
        # Menyimpan status port secara dinamis
        if connection_status == 0:
            scan_results[port] = "OPEN"
        else:
            scan_results[port] = "CLOSED"
        s.close()
        
    return scan_results
