# FORAGE (Pashu Poshana)
### *AI-Powered Executive Command Center for Fodder Security*

![Project Banner](https://img.shields.io/badge/Status-Production%20Ready-success) ![Tech](https://img.shields.io/badge/Built%20With-FastAPI%20%7C%20Tailwind%20%7C%20Chart.js-blue) ![AI](https://img.shields.io/badge/AI--Engine-STARK%20NLU-orange)

**FORAGE** (Pashu Poshana) is a state-of-the-art decision-support platform designed for the Department of Animal Husbandry. It unifies siloed agricultural supply data and livestock census demand into a single **Sufficiency Index**. Using predictive modeling and conversational AI, FORAGE empowers administrators to move from reactive crisis management to proactive resource planning.

---

## 🚀 Core Pillars & Features

### 1. Executive Operations Dashboard
- **Live Sufficiency Index:** A standardized "Health Score" (0.0 to 1.0) for every district and for the entire state.
- **Resource Heatmap:** Instant visual identification of **Surplus Hubs (Safe)** and **Deficit Targets (Risk)**.
- **Dynamic Deep-Dive:** Interactive filtering from a statewide perspective down to specific district profiles with zero latency.

### 2. Predictive Intelligence & Stress Testing
- **6-Month Rolling Forecast:** A temporal model that predicts exactly in which month a district will hit a "Resource Zero" state based on monthly consumption burn rates.
- **"What-If" Scenario Analysis:** Officials can simulate environmental shocks, such as a **20% Rainfall Reduction**, and instantly visualize the impact on the state's fodder buffer.
- **Vulnerability Matrix:** Categorizes districts into Critical, Elevated, or Stable risk zones based on predictive stock depletion.

### 3. Pashu Sahayak (AI Co-Pilot)
- **STARK NLU Engine:** A custom-built, deterministic Natural Language Understanding engine that provides factual, data-grounded insights.
- **Logistics Recommendations:** The AI automatically identifies the best "Supply Hubs" (like West Godavari) and suggests specific redistribution volumes to bridge the gap in deficit districts.
- **Conversational Analytics:** Ask plain-English questions like *"Which crop is deficit in Kadapa?"* or *"What are our key features?"* to get executive summaries.

---

## 🔬 Scientific & Statistical Methodology

FORAGE is built on rigorous agricultural and livestock science:
*   **RGR Modeling:** Uses **Residue-to-Grain Ratios** (e.g., 1.3 for Paddy, 2.0 for Maize) to calculate actual usable fodder biomass from raw grain production.
*   **Metabolic Accounting:** Demand is calculated based on the **2024 Livestock Census**, applying a **2.5% Dry Matter (DM)** daily intake standard for adult cattle and buffaloes.
*   **Confidence Metrics:** Every insight includes a **Certainty Score** based on data reporting density, with a standard statistical error range of **±8.5%** accounted for in governance buffers.

---

## 🛠️ Technical Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | HTML5, Tailwind CSS | Premium, responsive "Government SaaS" UI. |
| **Data Viz** | Chart.js, D3.js | Interactive Sunbursts, Area Charts, and Heatmaps. |
| **Backend** | FastAPI (Python) | High-concurrency API with asynchronous data handlers. |
| **Intelligence** | STARK NLU / RAG | Grounded AI logic for zero-hallucination responses. |
| **Data Tier** | Optimized CSV | High-speed, edge-ready data aggregates (No-DB approach). |

---

## 📂 Project Architecture

```bash
📦 pashu-poshana
 ┣ 📂 api                   # Intelligence & API Layer
 ┃ ┣ 📜 index.py            # API Entry Point & Data Normalization
 ┃ ┗ 📜 ai_engine.py        # STARK NLU, Forecasting & Scenario Logic
 ┣ 📜 index.html            # Main SPA Interface (Frontend)
 ┣ 📜 calculate_*.py        # Raw-to-Biomass Processing Pipeline
 ┣ 📜 requirements.txt      # Optimized Python Dependencies
 ┣ 📜 vercel.json           # Cloud Deployment Manifest
 ┣ 📜 run_local_server.bat  # 1-Click Launch (Windows)
 ┗ 📜 *.csv                 # Scientific Data Layers (Ground Truth)
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.9+

### Execution
1. **1-Click Launch (Windows):**
   Run `run_local_server.bat`. It will automatically configure the environment, install dependencies, and launch the dashboard.
   
2. **Access:**
   Navigate to `http://localhost:8000` in your browser.

---

## ☁️ Deployment
This project is production-ready for **Vercel** or any cloud provider.
- **Vercel:** Just import the GitHub repo; the `vercel.json` handles the rest.
- **On-Premise:** Can be run on a local government server without an internet connection, ensuring 100% data sovereignty.

---

**Developed for the Department of Animal Husbandry.**
*Bridging the gap between the field and the office with Data Intelligence.*
