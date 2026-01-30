import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import chatbot_module

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Forage",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED PROFESSIONAL STYLING ---
# --- SAAS MODERN DESIGN SYSTEM (v4.0) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    :root {
        --brand: #6366f1; /* Indigo */
        --brand-light: #e0e7ff;
        --content: #0f172a;
        --secondary: #64748b;
        --bg: #ffffff;
        --surface: #ffffff;
        --border: #f1f5f9;
        --radius: 20px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg);
        font-family: 'Outfit', sans-serif;
        color: var(--content);
    }

    /* Minimal Command Sidebar */
    [data-testid="stSidebar"] {
        background-color: #fafafa !important;
        border-right: 1px solid var(--border);
    }
    
    .sidebar-label {
        color: var(--secondary);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 2rem 0 0.5rem 0;
    }

    /* Floating SaaS Header */
    .saas-header {
        padding: 3rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--border);
    }
    .saas-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #0f172a 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Bento Box Metric Cards */
    .bento-card {
        background: var(--surface);
        padding: 2rem;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
        height: 100%;
    }

    .bento-card:hover {
        border-color: var(--brand);
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.1);
        transform: translateY(-5px);
    }

    .bento-label { 
        color: var(--secondary); 
        font-size: 0.85rem; 
        font-weight: 600; 
    }
    .bento-value { 
        color: var(--content); 
        font-size: 2.8rem; 
        font-weight: 800; 
        margin: 0.5rem 0;
        letter-spacing: -1.5px;
    }
    .bento-status { 
        font-size: 0.85rem; 
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: var(--brand);
    }

    /* Modern Tab Strip */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #f8fafc;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        color: var(--secondary) !important;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background: white !important;
        color: var(--brand) !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
    }

    /* Clean Alerts */
    .saas-alert {
        padding: 1.25rem 2rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 1rem;
        border: 1px solid transparent;
    }
    .alert-indigo { background: #eef2ff; color: #4338ca; border-color: #c7d2fe; }
    .alert-rose { background: #fff1f2; color: #be123c; border-color: #fecdd3; }
    .alert-emerald { background: #ecfdf5; color: #047857; border-color: #a7f3d0; }

    /* Hide Sidebar User info */
    section[data-testid="stSidebar"] .st-emotion-cache-1wf86c2 { display: none; }
    
    /* Global Section Spacing */
    .stPlotlyChart {
        background: white;
        border-radius: var(--radius);
        padding: 1rem;
        border: 1px solid var(--border);
    }
</style>
""", unsafe_allow_html=True)

# --- DATA NORMALIZATION ---
DISTRICT_MAPPING = {
    'SPSRNELLORE': 'NELLORE', 'SPSNELLORE': 'NELLORE', 'NELLORE': 'NELLORE',
    'YSRKADAPA': 'KADAPA', 'KADAPA': 'KADAPA', 'YSR': 'KADAPA',
    'ANANTHAPURAMU': 'ANANTAPUR', 'ANANTHAPUR': 'ANANTAPUR',
    'ALLURISITARAMARAJU': 'ALLURI SITARAMA RAJU', 'SRISATYASAI': 'SRI SATYASAI',
    'DRBRAMBEDKARKONASEEMA': 'DR B.R. AMBEDKAR KONASEEMA', 'PARVATHIPURAMMANYAM': 'PARVATHIPURAM MANYAM'
}

def normalize_name(name):
    if pd.isna(name): return ""
    clean = str(name).strip().upper().replace(" ", "").replace("-", "").replace(".", "")
    return DISTRICT_MAPPING.get(clean, clean)

@st.cache_data
def load_data():
    try:
        gap_df = pd.read_csv("fodder_gap_analysis.csv")
        supply_df = pd.read_csv("district_fodder_supply.csv")
        demand_df = pd.read_csv("district_fodder_demand.csv")
        mandal_demand_df = pd.read_csv("mandal_fodder_demand.csv")
        
        # Clean labels
        for df in [gap_df, supply_df, demand_df, mandal_demand_df]:
            df['District'] = df['District'].apply(normalize_name)
        
        # Unique district records for main summary
        gap_df = gap_df.drop_duplicates(subset=['District'])
        supply_df = supply_df.drop_duplicates(subset=['District'])
        demand_df = demand_df.drop_duplicates(subset=['District'])
        
        return gap_df, supply_df, demand_df, mandal_demand_df
    except Exception as e:
        st.error(f"Critical Data Load Error: {e}")
        return None, None, None, None

gap_df, supply_df, demand_df, mandal_demand_df = load_data()
if gap_df is None: st.stop()

# --- UTILS ---
def render_kpi(label, value, subtext="", color="#6366f1"):
    st.markdown(f"""
    <div class="bento-card">
        <div class="bento-label">{label}</div>
        <div class="bento-value">{value}</div>
        <div class="bento-status" style="color:{color}"><span>●</span> {subtext}</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.markdown('<div style="padding-bottom: 2rem;"><h1 style="color: var(--brand); margin:0; font-weight: 800; letter-spacing: -1.5px;">Forage</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-label">Global Filters</p>', unsafe_allow_html=True)
    
    unique_districts = sorted(gap_df['District'].unique().tolist())
    sel_dist = st.selectbox("Select District Entity", ["All Districts"] + unique_districts)
    
    if sel_dist == "All Districts":
        m_options = ["All Mandals"] + sorted(mandal_demand_df['Mandal'].unique().tolist())
    else:
        m_options = ["All Mandals"] + sorted(mandal_demand_df[mandal_demand_df['District'] == sel_dist]['Mandal'].unique().tolist())
    
    sel_mandal = st.selectbox("Select Mandal Subdivision", m_options)

    st.markdown('<p class="sidebar-label">INTELLIGENCE SERVICES</p>', unsafe_allow_html=True)
    chatbot_module.render_chatbot()
    
    st.markdown('<p class="sidebar-label">SYSTEM STATUS</p>', unsafe_allow_html=True)
    st.info("✅ Core Data Pipeline: Online\n\n✅ AI Model (Gemma 3): Ready")

# --- SAAS HEADER ---
st.markdown(f"""
    <div class="saas-header">
        <h1>Forage</h1>
        <p style="font-size: 1.25rem; color: var(--secondary); font-weight: 500;">
            Evidence-based decision support for livestock fodder security across Andhra Pradesh.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- ANALYTICAL TABS ---
t1, t2, t3, t4 = st.tabs(["🏛️ MAIN STATUS", "🌾 WHERE IS FOOD COMING FROM?", "🐄 WHO NEEDS FOOD?", "📊 CUSTOM ANALYSIS"])

# CALCULATE CONTEXT GLOBALS
tot_state_supply = gap_df['Total_Fodder_Tons'].sum()
tot_state_demand = gap_df['Total_Demand_Tons'].sum()

with t1:
    cols = st.columns(4)
    
    if sel_mandal != "All Mandals":
        # MANDAL VIEW
        m_data = mandal_demand_df[mandal_demand_df['Mandal'] == sel_mandal].iloc[0]
        parent_dist = m_data['District']
        d_data = gap_df[gap_df['District'] == parent_dist].iloc[0]
        
        # Estimate supply proportionate to demand ratio (best proxy available)
        m_ratio = m_data['Total_Demand_Tons'] / d_data['Total_Demand_Tons'] if d_data['Total_Demand_Tons'] > 0 else 0
        m_supply_est = d_data['Total_Fodder_Tons'] * m_ratio
        m_gap = m_supply_est - m_data['Total_Demand_Tons']
        m_adeq = (m_supply_est / m_data['Total_Demand_Tons'] * 100) if m_data['Total_Demand_Tons'] > 0 else 0
        
        with cols[0]: render_kpi("Food Needed", f"{m_data['Total_Demand_Tons']:.0f} T")
        with cols[1]: render_kpi("Food Available", f"{m_supply_est:.0f} T", f"From {parent_dist}")
        with cols[2]: render_kpi("Difference", f"{m_gap:.0f} T", f"{m_adeq:.1f}% Score", "#ef4444" if m_gap < 0 else "#059669")
        with cols[3]: render_kpi("Selected Area", sel_mandal, parent_dist)
        
        if m_gap < 0:
            st.markdown(f"""<div class="saas-alert alert-rose">🚨 <b>Observed Deficit:</b> Scenario analysis indicates {sel_mandal} requires ~{abs(m_gap):,.0f} tons of additional fodder for equilibrium.</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="saas-alert alert-emerald">✅ <b>Status Resilient:</b> {sel_mandal} is currently operating with a projected supply surplus.</div>""", unsafe_allow_html=True)
        main_score = m_adeq

    elif sel_dist != "All Districts":
        # DISTRICT VIEW
        d_data = gap_df[gap_df['District'] == sel_dist].iloc[0]
        with cols[0]: render_kpi("Food Available", f"{d_data['Total_Fodder_Tons']:.2f} T")
        with cols[1]: render_kpi("Food Needed", f"{d_data['Total_Demand_Tons']:.2f} T")
        with cols[2]: render_kpi("Difference", f"{d_data['Balance_Tons']:.0f} T", f"{d_data['Deficit_Percentage']:.1f}% Variance", "#ef4444" if d_data['Balance_Tons'] < 0 else "#059669")
        with cols[3]: render_kpi("Status", d_data['Status'], "District Level")
        
        if d_data['Balance_Tons'] < 0:
            st.markdown(f"""<div class="saas-alert alert-rose">🚨 <b>Critical Shortage Profile:</b> {sel_dist} is exhibiting a significant fodder deficit. Evidence-based intervention recommended.</div>""", unsafe_allow_html=True)
        main_score = (d_data['Total_Fodder_Tons'] / d_data['Total_Demand_Tons'] * 100) if d_data['Total_Demand_Tons'] > 0 else 0
    else:
        # STATE VIEW
        with cols[0]: render_kpi("Food Available", f"{tot_state_supply/1e6:.2f}M T")
        with cols[1]: render_kpi("Food Needed", f"{tot_state_demand/1e6:.2f}M T")
        with cols[2]: render_kpi("Gap", f"{(tot_state_supply-tot_state_demand)/1e6:.2f}M T", "Critical Shortage", "#ef4444")
        with cols[3]: render_kpi("Red Districts", f"{len(gap_df[gap_df['Status']=='DEFICIT'])} Areas", "Vulnerability Detected")
        st.markdown("""<div class="saas-alert alert-indigo">✨ <b>Governance Decision Signal:</b> Heuristic analysis indicates a potential supply-demand imbalance. Consider routing surplus from Coastal regions to Rayalaseema.</div>""", unsafe_allow_html=True)
        main_score = (tot_state_supply / tot_state_demand * 100) if tot_state_demand > 0 else 0

    # CHARTS (Simplified for Layman)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📊 District Fodder Balance (Surplus vs Deficit)")
        # Create a categorical color column for clarity
        gap_df_display = gap_df.sort_values('Balance_Tons').copy()
        gap_df_display['Status'] = gap_df_display['Balance_Tons'].apply(lambda x: 'Enough Food' if x > 0 else 'Shortage')
        
        fig_map = px.bar(gap_df_display, x='District', y='Balance_Tons', 
                         color='Status',
                         color_discrete_map={'Enough Food': '#10b981', 'Shortage': '#f43f5e'},
                         labels={'Balance_Tons': 'Amount (Tons)', 'District': 'District'},
                         template='plotly_white')
        
        fig_map.update_layout(
            height=500, 
            margin=dict(t=20, b=100, l=10, r=10),
            xaxis_tickangle=-45,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Outfit", size=12),
            legend_title_text='Status'
        )
        st.plotly_chart(fig_map, width='stretch')
        
    with c2:
        st.subheader("🔍 Statutory Security Gauge")
        # Simplified Gauge for Layman
        gauge_color = "#dc2626" if main_score < 60 else "#f59e0b" if main_score < 100 else "#059669"
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = main_score,
            number = {'suffix': "%", 'font': {'size': 60, 'color': '#0f172a', 'family': 'Plus Jakarta Sans'}},
            gauge = {
                'axis': {'range': [0, 150], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 60], 'color': "#fff1f2"},
                    {'range': [60, 100], 'color': "#fffbeb"},
                    {'range': [100, 150], 'color': "#f0fdf4"}]
            }
        ))
        fig_gauge.update_layout(height=400, margin=dict(t=50, b=0, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_gauge, width='stretch')

with t2:
    st.subheader("🌾 Agricultural Supply Diagnostics")
    st.markdown("Breakdown of fodder supply by primary crop source across the state and selected regions.")
    
    crop_cols = [c for c in supply_df.columns if c not in ['District', 'Total_Fodder_Tons', 'District_Key']]
    # Use a vivid multi-color palette
    agri_palette = px.colors.qualitative.Vivid
    
    if sel_dist == "All Districts":
        st.markdown("### 🌍 All Crops in the State")
        state_totals = supply_df[crop_cols].sum().sort_values(ascending=False)
        
        # Simple Bar Chart for visual summary
        fig_st_crops = px.bar(
            state_totals.reset_index().rename(columns={'index': 'Crop Name', 0: 'Amount (Tons)'}),
            y='Crop Name', x='Amount (Tons)',
            orientation='h',
            color='Crop Name',
            color_discrete_sequence=agri_palette,
            text_auto='.2s',
            template='plotly_white'
        )
        fig_st_crops.update_layout(showlegend=False, height=500, margin=dict(t=20, b=20, l=150))
        st.plotly_chart(fig_st_crops, width='stretch')

        st.markdown("#### 📋 Detailed List of Food Sources")
        # Display as a clean, sorted table for easy reading
        st.dataframe(state_totals.reset_index().rename(columns={'index': 'Crop Name', 0: 'Total Food (Tons)'}), 
                     width='stretch', height=400)
    else:
        st.markdown(f"### 📍 Local Crops in: {sel_dist}")
        dist_row = supply_df[supply_df['District'] == sel_dist].iloc[0]
        dist_vals = dist_row[crop_cols].sort_values(ascending=False)
        dist_vals = dist_vals[dist_vals > 0]
        
        cc1, cc2 = st.columns([2, 1])
        with cc1:
            # Horizontal bar is more layman friendly as names don't overlap
            fig_h = px.bar(dist_vals, orientation='h', 
                           color=dist_vals.index, 
                           color_discrete_sequence=agri_palette,
                           labels={'value': 'Available Tons', 'index': 'Crop Type'},
                           text_auto='.2s')
            fig_h.update_layout(showlegend=False, height=500, margin=dict(t=20, b=20))
            st.plotly_chart(fig_h, width='stretch')
        with cc2:
            # Pie with distinct colors
            fig_p = px.pie(values=dist_vals.values, names=dist_vals.index, 
                           hole=0.6, color_discrete_sequence=agri_palette)
            fig_p.update_layout(height=500, margin=dict(t=0, b=0))
            st.plotly_chart(fig_p, width='stretch')

with t3:
    st.subheader("🐄 Livestock Demand Profile")
    st.markdown("Categorized livestock fodder requirements based on species and census data.")
    
    animal_cols = [c for c in demand_df.columns if '_Demand' in c]
    animal_palette = px.colors.qualitative.Pastel
    
    if sel_mandal != "All Mandals":
        m_row = mandal_demand_df[mandal_demand_df['Mandal'] == sel_mandal].iloc[0]
        # Clean animal names for layman
        m_vals = m_row[animal_cols]
        m_vals.index = [c.replace('_Demand','') for c in m_vals.index]
        m_vals = m_vals.sort_values(ascending=False)
        
        cc1, cc2 = st.columns([1, 1])
        with cc1:
             st.markdown(f"#### 📊 Animals in {sel_mandal}")
             st.plotly_chart(px.pie(values=m_vals.values, names=m_vals.index, 
                                     hole=0.6, color_discrete_sequence=animal_palette), width='stretch')
        with cc2:
             st.markdown("#### 📋 How much food they need")
             st.table(m_vals.reset_index().rename(columns={'index': 'Animal Name', 0: 'Food Needed (Tons)'}))
    elif sel_dist != "All Districts":
        dist_mandals = mandal_demand_df[mandal_demand_df['District'] == sel_dist]
        st.markdown(f"#### 🏘️ Areas with most animals in {sel_dist}")
        # Use horizontal bar to prevent label overlapping for mandals (which can be many)
        fig_m = px.bar(dist_mandals.sort_values('Total_Demand_Tons', ascending=False).head(15), 
                       y='Mandal', x='Total_Demand_Tons', 
                       orientation='h',
                       color='Mandal',  # Each mandal gets a color for vibrancy
                       color_discrete_sequence=px.colors.qualitative.T10,
                       text_auto='.2s',
                       labels={'Total_Demand_Tons': 'Food Needed (Tons)'})
        fig_m.update_layout(height=600, showlegend=False, margin=dict(l=150))
        st.plotly_chart(fig_m, width='stretch')
    else:
        st.markdown("### 🗺️ Where Animals are in the State")
        # Cleaner animal names for legend
        demand_df_clean = demand_df.copy()
        demand_df_clean.columns = [c.replace('_Demand','') for c in demand_df_clean.columns]
        clean_animal_cols = [c.replace('_Demand','') for c in animal_cols]
        
        fig_st = px.bar(demand_df_clean, x='District', y=clean_animal_cols, 
                         title="Types of Animals in Each District", 
                         labels={'value': 'Food Needed (Tons)', 'variable': 'Animal Type'},
                         barmode='stack', 
                         color_discrete_sequence=px.colors.qualitative.Prism)
        fig_st.update_layout(xaxis_tickangle=-45, height=600, margin=dict(b=120))
        st.plotly_chart(fig_st, width='stretch')

with t4:
    st.subheader("📊 Personal Data Analytics Sandbox")
    st.markdown("Upload your own Animal or Agricultural dataset (CSV/Excel) to get instant visual insights and AI help.")
    
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                u_df = pd.read_csv(uploaded_file)
            else:
                u_df = pd.read_excel(uploaded_file)
            
            st.session_state['custom_file_data'] = u_df
            
            st.success(f"✅ Successfully loaded '{uploaded_file.name}'")
            
            # Overview Metrics
            uc1, uc2, uc3 = st.columns(3)
            with uc1: render_kpi("Total Records", len(u_df))
            with uc2: render_kpi("Columns Found", len(u_df.columns))
            with uc3: render_kpi("Numeric Fields", len(u_df.select_dtypes(include=['number']).columns))
            
            # Data Preview
            with st.expander("👀 View Raw Data Preview", expanded=False):
                st.dataframe(u_df, width='stretch')
            
            # Automatic Visualization Engine
            st.divider()
            st.markdown("### 📈 Automated Insights")
            
            num_cols = u_df.select_dtypes(include=['number']).columns.tolist()
            cat_cols = u_df.select_dtypes(exclude=['number']).columns.tolist()
            
            if num_cols and cat_cols:
                v1, v2 = st.columns(2)
                with v1:
                    # Bar Chart
                    st.markdown(f"**Comparison: {cat_cols[0]} vs {num_cols[0]}**")
                    fig_u_bar = px.bar(u_df.head(20), x=cat_cols[0], y=num_cols[0], color=cat_cols[0], template="plotly_white")
                    st.plotly_chart(fig_u_bar, width='stretch')
                with v2:
                    # Comparison Pie
                    st.markdown(f"**Distribution: {cat_cols[0]}**")
                    fig_u_pie = px.pie(u_df.head(10), names=cat_cols[0], values=num_cols[0], hole=0.5)
                    st.plotly_chart(fig_u_pie, width='stretch')
            else:
                st.info("Upload a dataset with both text and number columns to unlock automated charts.")

        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Waiting for file upload... (Supports .csv and .xlsx)")

# --- INSTITUTIONAL FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
with f_col1:
    st.markdown("""
        <div style="opacity: 0.6; font-size: 0.8rem;">
            <b>Forage Enterprise Fodder DSS</b><br>
            © 2026 Department of Animal Husbandry & Fodder Security.<br>
            Designed for data-driven administrative decision making.
        </div>
    """, unsafe_allow_html=True)
with f_col2:
    st.markdown("""
        <div style="opacity: 0.6; font-size: 0.8rem;">
            <b>DATA SOURCES</b><br>
            Livestock Census 2024<br>
            Land Utilization Records
        </div>
    """, unsafe_allow_html=True)
with f_col3:
    st.markdown("""
        <div style="text-align: right; opacity: 0.6; font-size: 0.8rem;">
            <b>SYSTEM VERSION</b><br>
            Build: 2.0.4-PRO<br>
            Engine: Ollama/Gemma3
        </div>
    """, unsafe_allow_html=True)
