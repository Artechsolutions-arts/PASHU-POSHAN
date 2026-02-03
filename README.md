# FORAGE (Pashu Poshana)
### *Institutional Analytics Dashboard for Fodder Security*

![Project Banner](https://img.shields.io/badge/Status-Production%20Ready-success) ![Tech](https://img.shields.io/badge/Built%20With-FastAPI%20%7C%20Tailwind%20%7C%20Chart.js-blue)

**Forage** (branded as **pashuposhana**) is a real-time command center designed for the Department of Animal Husbandry. It aggregates agricultural supply data and livestock census demand data to provide a unified **Sufficiency Index** for every district. This tool empowers officials to predict fodder shortages, optimize resource allocation, and ensure zero starvation days for livestock.

---

## 🚀 Key Features

### 1. Executive Operations Center
- **Live Net Gap Analysis:** Instant visual indicators of **Surplus (Green)** vs **Deficit (Red)** districts.
- **Sufficiency Index:** A single standardized score (0-100) to measure regional food security.
- **Dynamic Filtering:** Drill down from State-level overview to specific Districts.

### 2. Deep-Dive Analytics
- **Supply Profile:** Breakdown of biomass sources (Paddy, Maize, Groundnut) using interactive **Sunburst Charts**.
- **Demand Dynamics:** Analysis of livestock consumption patterns (Cattle vs Buffalo vs Small Ruminants).
- **Mandal Register:** Hyper-local view of demand at the sub-district (Mandal) level.

### 3. Predictive Intelligence (AI)
- **6-Month Forecast:** Trend line projections for future fodder availability vs demand.
- **Vulnerability Alerts:** Early warning system for districts facing upcoming shortages.
- **Pashu Sahayak (AI Bot):** An embedded AI assistant that answers plain-English queries about the data and suggests logistical stockpiling strategies.

---

## 🛠️ Technical Architecture

This project is built as a high-performance **Single Page Application (SPA)** backed by a robust Python API.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, Tailwind CSS | Responsive, mobile-first UI with a "Clean Govt" aesthetic. |
| **Visualization** | Chart.js, Plotly.js | Zero-latency rendering of complex datasets. |
| **Backend** | FastAPI (Python) | High-speed API for data processing and AI logic. |
| **Data Engine** | Pandas, NumPy | vectorized calculations for gap analysis. |
| **AI Engine** | Hybrid (Ollama + Logic) | Intelligent fallback system (Cloud-Safe Logic + Local LLM). |

---

## 📂 Project Structure

```bash
📦 pashu-poshana
 ┣ 📂 api                   # Backend Logic
 ┃ ┣ 📜 index.py            # Main FastAPI Entry Point
 ┃ ┗ 📜 ai_engine.py        # AI Chatbot & Forecasting Logic
 ┣ 📜 index.html            # Main Dashboard Interface (Frontend)
 ┣ 📜 calculate_*.py        # Data Processing Scripts (Supply/Demand/Gap)
 ┣ 📜 requirements.txt      # Python Dependencies (Optimized for Cloud)
 ┣ 📜 vercel.json           # Deployment Configuration
 ┣ 📜 run_local_server.bat  # 1-Click Launch Script for Windows
 ┗ 📜 *.csv                 # Data Layers (Supply, Demand, Gap Analysis)
```

---

## ⚡ Quick Start (Run Locally)

### Prerequisites
- Python 3.9+ installed.

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/forage-pashuposhana.git
   cd forage-pashuposhana
   ```

2. **Run the 1-Click Script (Windows):**
   Double-click `run_local_server.bat` 
   *(This script automatically sets up the virtual environment, installs dependencies, and launches the server).*

3. **Manual Setup (Mac/Linux):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn api.index:app --reload
   ```

4. **Access the Dashboard:**
   Open your browser and navigate to: `http://localhost:8000`

---

## ☁️ Deployment (Vercel)

This project is configured for **0-Config Deployment** on Vercel.

1. Push the code to GitHub.
2. Import the repository in Vercel.
3. Click **Deploy**.
   - *Note: The Vercel build will automatically use the `api/index.py` entry point.*

---

## 🛡️ Governance & Data Logic
- **"Surplus" Definition:** When gross fodder supply > calculated dry matter demand.
- **"Deficit" Definition:** When nutritional demand > available biomass.
- **Forecast Model:** Uses a 6-month moving trend based on historical harvest indices and census growth rates.

---

**Developed for the Department of Animal Husbandry.**
*Ensuring that no animal goes hungry when data can feed them.*
