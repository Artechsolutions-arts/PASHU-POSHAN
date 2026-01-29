# Cloud Deployment Guide (Vercel)

This guide explains how to deploy the **Forage Dashboard** to the cloud using Vercel. This allows you to share the dashboard via a public URL.

## ⚠️ Important Limitations
1.  **AI Chatbot**: The "Pashu Sahayak" chatbot uses a local AI model (Ollama). On the cloud deployment, it will **NOT** be able to access your local AI. It will fall back to "Local Logic Mode" (keyword matching) unless you configure a cloud-based LLM (like Groq or OpenAI).
2.  **Read-Only**: The cloud version is read-only. You cannot upload new files to update the dataset permanently.

## Prerequisites
1.  **Node.js**: REQUIRED to install Vercel CLI. [Download Node.js (LTS)](https://nodejs.org/)
2.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com/signup).

## Step-by-Step Deployment

### 1. Install Vercel CLI
Open your terminal (PowerShell or Command Prompt) and run:
```powershell
npm install -g vercel
```

### 2. Login to Vercel
Run the following command and follow the on-screen instructions to authorize:
```powershell
vercel login
```

### 3. Deploy
Run the deployment command from the project folder:
```powershell
vercel --prod
```

### 4. Configure Deployment (First Time Only)
The CLI will ask you a few questions. Answer them as follows:
-   **Set up and deploy?**: `Y`
-   **Which scope?**: (Select your account)
-   **Link to existing project?**: `N`
-   **Project Name**: `pashu-poshana` (or leave default)
-   **In which directory is your code located?**: `./` (Just press Enter)
-   **Want to modify these settings?**: `N` (Just press Enter)

The system will now build and deploy your app. This may take 1-2 minutes.
Once finished, it will give you a **Production** URL (e.g., `https://pashu-poshana.vercel.app`).

## Verifying Deployment
Open the provided URL in your browser.
1.  Check if the dashboards load (Charts, Maps).
2.  Test the filtering.
3.  Note that the AI chat will function in "Fallback Mode".

## Troubleshooting
-   **"504 Gateway Timeout"**: If the initial load takes too long, refresh the page.
-   **"Function Size Too Large"**: If the deployment fails due to size, edit `requirements.txt` to remove unused heavy libraries like `torch` or `streamlit` (only `fastapi`, `pandas`, `plotly` are strictly needed for the web version).
