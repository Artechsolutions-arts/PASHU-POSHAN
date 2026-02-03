# How to Deploy FORAGE Dashboard to Vercel

## Option 1: Using Github (Recommended)
1. Push this entire folder to a GitHub repository.
2. Go to [Vercel.com](https://vercel.com) and log in.
3. Click **"Add New Project"** and select your GitHub repository.
4. Vercel will detect the `vercel.json` and deploy automatically.
   - **Framework Preset:** Other (or FastAPI if detected)
   - **Root Directory:** `./`

## Option 2: Using Command Line (CLI)
1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```
2. Run the deploy command from this folder:
   ```bash
   vercel
   ```
3. Follow the prompts (Keep all default settings).

## Option 3: Using Railway (Best for Always-On)
1. Push this code to **GitHub**.
2. Go to [Railway.app](https://railway.app) and "Start a New Project".
3. Select **"Deploy from GitHub repo"**.
4. Choose your repository.
5. Railway will detect the `Procfile` and deploy automatically.
   - **Note:** If asked for a start command, use: `uvicorn api.index:app --host 0.0.0.0 --port $PORT`

## Important Notes
- **AI Features:** The cloud deployment uses a "Safe Mode" AI because heavy LLMs (Ollama) cannot run on Vercel's free tier. The fallback engine uses pre-calculated insights which is faster and more reliable for web users.
- **Data:** All CSV files in the root folder are automatically included.
