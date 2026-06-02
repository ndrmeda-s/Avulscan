<div align="center">

<h1>Automated Vulnerability Scanner</h1>

<img src="./assets/banner.gif" width="600" height="240" alt="Vulnerability Scanner Banner"/>

Modular Full-Stack Security Assessment Tool built with **FastAPI** and **Docker**.

[![Python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Vercel](https://img.shields.io/badge/vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com/)

</div>

---

# Description

**Avulscan** is a full-stack security assessment tool designed for educational use on 
pre-authorized assets. Leveraging **FastAPI** and **Docker**, it modularly scans for open 
ports, evaluates HTTP security headersecurity, and outputs PDF audit reports. Compatible 
with Desktop and Termux environments.

---

# Key Features

* **Network Port Scanning:** Real-time checking for core network infrastructure ports (`21`, `22`, `80`, `443`).
* **HTTP Security Headers Analysis:** Live inspection of crucial defense headers (`HSTS`, `CSP`, `X-Frame-Options`, `X-Content-Type-Options`).
* **Stealth & Bypass Engine:** Armed with an unverified SSL Context to prevent certificate crashes and a customized real-browser User-Agent to bypass restrictive Web Application Firewalls (WAF).
* **Enterprise PDF Reporter:** Automatically compiles raw security metrics into a formal audit PDF document featuring dynamically drawn vector progress bars and comprehensive informatics definitions.
* **Hard Whitelist Security:** Built-in network guardrails restricting scans strictly to verified testing laboratories (`scanme.nmap.org`, `github.com`, and `sayuran.vip`) to comply with legal frameworks.

---

# Tech Stack

### Backend (API Engine)
* **Python 3.13** - Core application logic
* **FastAPI** - Modern, high-performance web framework for building APIs
* **Uvicorn** - Lightning-fast ASGI server implementation
* **FPDF2** - Advanced PDF creation library with vector shape manipulation

### Frontend (User Dashboard)
* **HTML5 & Vanilla JavaScript** - Asynchronous API fetching and dynamic DOM injection
* **Tailwind CSS (via CDN)** - Modern, utility-first utility class framework for responsive dark-mode styling

---

## Project Architecture

```
 avulscan/
 ├── backend/
 │   ├── app.py                # Main FastAPI Gateway & Whitelist Security
 │   ├── requirements.txt      # Backend Python dependencies
 │   └── core/
 │       ├── scanner.py        # TCP Socket connection scanner
 │       ├── header_scan.py    # Stealth HTTP header analyzer
 │       └── reporter.py       # Vector PDF report generator engine
 └── frontend/
     ├── index.html            # Dark-mode dashboard UI
     └── js/
         └── app.js            # Fetch API integration handler
```

---

# How to Setup and Run Locally
​Prerequisites (For Termux/Android users)
​Ensure you have the required compilers to build modern Python rust-based wheels:

```
pkg update && pkg upgrade -y
pkg install clang make rust python -y
export ANDROID_API_LEVEL=24
```

---

## 1. Backend Deployment

Navigate to the backend directory, install dependencies, and fire up the Uvicorn server:

```
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

The API engine will stand by at http://localhost:8080.

---

## ​2. Frontend Deployment

​Open a New Session in Termux, navigate to the frontend directory, and run a lightweight local HTTP server:

```
cd frontend
python -m http.server 8000
```

Open your browser and access the interactive dashboard at: http://localhost:8000.

---

## License & Terms of Use

This project uses a dual-license model:

**1. Frontend - MIT License**  
Code under `frontend/` is licensed under MIT. See `frontend/LICENSE`.

**2. Backend - Apache License 2.0 + Ethical Use Terms**  
Code under `backend/` is licensed under Apache 2.0. See `backend/LICENSE`. 

**By using any part of this software, you agree to the following binding terms:**

1. **Authorized Use Only**: This tool is for educational purposes and authorized security testing ONLY. You may only scan systems you own or have explicit written permission to test.
2. **No Illegal Activity**: Unauthorized network scanning may violate laws such as UU ITE in Indonesia. Any illegal use immediately terminates your license to this software.
3. **Whitelist Enforcement**: The backend has a hard-coded whitelist: `scanme.nmap.org`, `github.com`, `avulscan.vercel.app`, `sayuran.vip`. Attempts to bypass it are prohibited.
4. **No Warranty & Liability**: The software is provided "AS IS". Developers assume no liability for damages or legal consequences arising from misuse.

Violation of these terms constitutes copyright infringement.

---
