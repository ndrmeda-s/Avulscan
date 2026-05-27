document.getElementById('scanBtn').addEventListener('click', async () => {
    const target = document.getElementById('targetSelect').value;
    const scanBtn = document.getElementById('scanBtn');
    const loadingState = document.getElementById('loadingState');
    const resultsState = document.getElementById('resultsState');
    
    // Alamat URL API lokal FastAPI kita di Termux
    const API_BASE_URL = "http://localhost:8080";

    // 1. Mengubah tampilan UI ke mode Loading
    scanBtn.disabled = true;
    loadingState.classList.remove('hidden');
    resultsState.classList.add('hidden');

    try {
        // 2. Menembak API Scan Backend menggunakan Fetch
        const response = await fetch(`${API_BASE_URL}/api/scan?target=${target}`);
        
        if (!response.ok) {
            throw new Error('Scan process failed on server.');
        }

        const data = await response.json();

        // 3. Merender Data Hasil Scan Port
        const portGrid = document.getElementById('portGrid');
        portGrid.innerHTML = ''; // Reset grid lama
        
        for (const [port, status] of Object.entries(data.ports_status)) {
            const isBlue = status === 'OPEN';
            portGrid.innerHTML += `
                <div class="p-4 rounded-lg bg-slate-950 text-center border ${isBlue ? 'border-indigo-500/40' : 'border-slate-700'}">
                    <span class="block text-xs font-semibold text-slate-400">PORT ${port}</span>
                    <span class="block text-sm font-bold mt-1 ${isBlue ? 'text-indigo-400' : 'text-slate-500'}">${status}</span>
                </div>
            `;
        }

        // 4. Merender Data Hasil Scan Security Headers
        const headerList = document.getElementById('headerList');
        headerList.innerHTML = ''; // Reset list lama
        
        for (const [header, status] of Object.entries(data.headers_status)) {
            const isSecure = status.includes('Secure');
            headerList.innerHTML += `
                <div class="flex justify-between items-center p-3 rounded-lg bg-slate-950 border ${isSecure ? 'border-emerald-500/20' : 'border-amber-500/20'}">
                    <span class="text-sm font-medium text-slate-300">${header}</span>
                    <span class="text-xs font-bold px-2.5 py-1 rounded-full ${isSecure ? 'bg-emerald-950 text-emerald-400' : 'bg-amber-950 text-amber-400'}">
                        ${status}
                    </span>
                </div>
            `;
        }

        // 5. Memasang tautan unduh dokumen PDF secara riil ke tombol download
        const downloadBtn = document.getElementById('downloadBtn');
        downloadBtn.href = `${API_BASE_URL}${data.pdf_report_url}`;

        // 6. Menampilkan kotak hasil ke layar dashboard
        resultsState.classList.remove('hidden');

    } catch (error) {
        alert(`[!] Error: ${error.message}`);
    } finally {
        // 7. Mengembalikan status tombol kembali normal
        scanBtn.disabled = false;
        loadingState.classList.add('hidden');
    }
});
