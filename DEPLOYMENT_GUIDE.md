# Forage Dashboard - Deployment Guide

This guide provides step-by-step instructions to deploy and run the Forage Dashboard on a Windows machine.

## Prerequisites

The following software is required to run the application:
1.  **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
    *   *Note: During installation, ensure you check the box "Add Python to PATH".*

## Setup Instructions

### 1. Verification
Open a new **Command Prompt** or **PowerShell** and verify Python is installed:
```powershell
python --version
```
If this returns a version number (e.g., `Python 3.12.0`), you are ready to proceed.

### 2. Install Dependencies
Navigate to the project directory and install the required Python packages:

```powershell
pip install streamlit pandas plotly python-dotenv langchain-groq langchain-core openpyxl
```

### 3. API Key Configuration
The application requires a Groq API key for the "Pashu Sahayak" AI chatbot.

1.  Open the file `.env` in the root of the project.
2.  Ensure it contains your valid API key in the following format:
    ```
    GROQ_API_KEY=gsk_your_actual_key_here...
    ```
    *(Note: Do not start the key with quotes)*

### 4. Running the Dashboard
To start the application, run the following command in your terminal:

```powershell
streamlit run dashboard.py
```

This will launch a local web server (usually at `http://localhost:8501`) and open the dashboard in your default web browser.

## Troubleshooting

-   **"python is not recognized"**: You might need to add Python to your system PATH or restart your terminal after installation.
-   **"ModuleNotFoundError"**: Run the `pip install` command again to ensure all libraries are installed.
-   **"Data files not found"**: If the dashboard says files are missing, run the following scripts in order to regenerate the data:
    ```powershell
    python calculate_fodder_supply.py
    python calculate_fodder_demand.py
    python calculate_gap_analysis.py
    ```

## Checking if it works
Once the dashboard opens:
1.  **Overview Page**: You should see "State-Level Overview" with metrics (Supply, Demand, Balance).
2.  **Map**: A bar chart showing surpluses and deficits by district.
3.  **Chatbot**: Scroll down to "Pashu Sahayak" and ask a question like "Which districts have a fodder deficit?" to test the AI integration.
