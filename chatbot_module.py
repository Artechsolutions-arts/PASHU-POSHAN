import streamlit as st
import pandas as pd
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()

# Using Ollama for local LLM - no API keys needed!
USE_OLLAMA = True  # Set to False to use OpenAI instead

def render_chatbot():
    # Load primary data
    try:
        df = pd.read_csv("fodder_gap_analysis.csv")
    except:
        df = None

    # Check for custom uploaded data
    custom_df = st.session_state.get('custom_file_data')



    # We'll use a standard Streamlit expander instead of complex JS for reliability
    with st.sidebar:
        st.divider()
        st.markdown("### Forage")
        with st.expander("💬 Ask me a question", expanded=False):
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("Ask me about fodder status..."):
                # Display user message in chat message container
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate Response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    
                    def get_local_response(prompt, df, custom_df=None):
                        clean_q = prompt.upper().replace("?", "").replace("!", "")
                        words = set(clean_q.split())
                        
                        # PRIORITY: Check custom uploaded data first if it exists
                        if custom_df is not None:
                            for col in custom_df.columns:
                                if col.upper() in clean_q:
                                    return f"In your uploaded file ('{st.session_state.get('uploaded_filename', 'data')}'), I found column **'{col}'**. I can see the data, but my AI brain needs more credits for a deep analysis."

                        # 0. Load supply data for crop questions
                        try:
                            supply_df = pd.read_csv("district_fodder_supply.csv")
                        except:
                            supply_df = None

                        # 1. Crop Specific Questions
                        if supply_df is not None:
                            crop_cols = [c for c in supply_df.columns if c not in ['District', 'Total_Fodder_Tons', 'District_Key']]
                            for crop in crop_cols:
                                if crop.upper() in clean_q:
                                    top_dist = supply_df.sort_values(crop, ascending=False).iloc[0]
                                    return f"The largest producer of **{crop}** is **{top_dist['District']}** with **{top_dist[crop]:,.0f} tons** available."

                        # 2. Greetings
                        if any(greet in words for greet in ["HELLO", "HI", "NAMASTE", "HELP"]):
                            return "Hello! I am **Forage**. I can help you find fodder status for districts or analyze your custom uploaded data."

                        # 3. Primary Data Logic (Fodder)
                        if df is not None:
                            if any(word in clean_q for word in ["STATE", "OVERVIEW", "SUMMARY", "WHOLE", "ALL"]):
                                tot_s = df['Total_Fodder_Tons'].sum()
                                tot_d = df['Total_Demand_Tons'].sum()
                                red_count = len(df[df['Status']=='DEFICIT'])
                                return f"State-wide summary: Total Available food is **{tot_s/1e6:.2f}M tons** against a need of **{tot_d/1e6:.2f}M tons**. There are **{red_count}** districts currently in shortage."

                            if any(word in clean_q for word in ["TOP", "BEST", "SURPLUS", "HIGHEST"]):
                                top = df.sort_values('Balance_Tons', ascending=False).iloc[0]
                                return f"The district with the best food status is **{top['District']}** with a surplus of **{top['Balance_Tons']:,.0f} tons**."
                            
                            if any(word in clean_q for word in ["WORST", "LOWEST", "SHORTAGE", "DEFICIT", "BAD"]):
                                worst = df.sort_values('Balance_Tons', ascending=True).iloc[0]
                                return f"The district in most need is **{worst['District']}** with a shortage of **{abs(worst['Balance_Tons']):,.0f} tons**."

                            for _, row in df.iterrows():
                                d_name = str(row['District']).upper().replace(" ", "")
                                if d_name in clean_q.replace(" ", ""):
                                    return f"Based on latest records, **{row['District']}** is in a **{row['Status']}** state with a balance of **{abs(row['Balance_Tons']):,.0f} tons**."
                        
                        return "I am currently in **Local Mode**. Please ask about a specific district, a crop, or upload your own file in the 'Custom Analysis' tab."

                    if USE_OLLAMA:
                        try:
                            llm = ChatOllama(model="gemma3:1b", temperature=0.1, base_url="http://localhost:11434")
                            active_data = custom_df if custom_df is not None else df
                            context = active_data.to_string(index=False) if active_data is not None else "No data."
                            
                            ai_prompt = f"""
                            Role: Senior AI Governance Engineer & Applied Data Scientist.
                            Context: {context}
                            Task: Analyze the user query using the Governance Decision Framework.
                            
                            Structural Priority:
                            - DESCRIPTIVE OBSERVATION: Fact-based status.
                            - DIAGNOSTIC REASONING: Data lineage & logic.
                            - ADVISORY RECOMMENDATION: Advisory scenario suggestions.
                            - CERTAINTY & ASSUMPTIONS: Disclosure of data quality & limits.
                            
                            Governance Constraint: Frame outcomes as support signals, not directives.
                            User Question: {prompt}
                            """
                            ai_response = llm.invoke(ai_prompt).content
                            
                            # Standardized Disclaimer Injection
                            ai_response += "\n\n*DISCLAIMER: This output is a Decision Support Signal intended for scenario-planning. Recommendations are advisory and must be validated against ground-truth signals.*"
                            
                            message_placeholder.markdown(ai_response)
                            st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        except Exception:
                            # Robust fallback to advanced local governance logic
                            from api.ai_engine import get_local_response
                            response = f"⚠️ [Local Governance Decision Integrity Active]\n\n" + get_local_response(prompt, df)
                            message_placeholder.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        from api.ai_engine import get_local_response
                        response = get_local_response(prompt, df)
                        message_placeholder.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
