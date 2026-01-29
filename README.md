# Forage
## API Key Configuration

To enable the AI chatbot, you need to provide a Groq API key:

1. **Get your API key:**
   - Visit [https://console.groq.com/keys](https://console.groq.com/keys)
   - Sign up or log in
   - Create a new API key

2. **Configure the .env file:**
   - Copy `.env.template` to `.env`:
     ```bash
     copy .env.template .env
     ```
   - Edit `.env` and replace `your_api_key_here` with your actual API key:
     ```
     GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```

3. **Run the dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

## Features

- **Fodder Gap Analysis**: View supply vs demand across all districts
- **Interactive Visualizations**: Charts and metrics for each district
- **AI Assistant (Forage AI)**: Ask questions about fodder management, crop planning, and livestock nutrition

## Note

Make sure `.env` is in your `.gitignore` to keep your API key secure!
