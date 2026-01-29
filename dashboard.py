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
    layout="wide"
)



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
def render_kpi(label, value):
    st.metric(label, value)

# --- SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.title("Forage")
    st.divider()
    
    unique_districts = sorted(gap_df['District'].unique().tolist())
    sel_dist = st.selectbox("Select District", ["All Districts"] + unique_districts)
    
    if sel_dist == "All Districts":
        m_options = ["All Mandals"] + sorted(mandal_demand_df['Mandal'].unique().tolist())
    else:
        m_options = ["All Mandals"] + sorted(mandal_demand_df[mandal_demand_df['District'] == sel_dist]['Mandal'].unique().tolist())
    
    sel_mandal = st.selectbox("Select Mandal", m_options)
    
    st.divider()
    chatbot_module.render_chatbot()

# --- SAAS HEADER ---
st.title("Fodder Analytics Dashboard")
st.markdown("Evidence-based decision support for livestock fodder security across Andhra Pradesh.")

# --- ANALYTICAL TABS ---
t1, t2, t3 = st.tabs(["🏛️ MAIN STATUS", "🌾 SUPPLY ANALYSIS", "🐄 DEMAND DYNAMICS"])

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
        with cols[1]: render_kpi("Food Available", f"{m_supply_est:.0f} T")
        with cols[2]: render_kpi("Difference", f"{m_gap:.0f} T")
        with cols[3]: render_kpi("Selected Area", sel_mandal)
        
        if m_gap < 0:
            st.error(f"🚨 **Observed Deficit:** Scenario analysis indicates {sel_mandal} requires ~{abs(m_gap):,.0f} tons of additional fodder for equilibrium.")
        else:
            st.success(f"✅ **Status Resilient:** {sel_mandal} is currently operating with a projected supply surplus.")
        main_score = m_adeq

    elif sel_dist != "All Districts":
        # DISTRICT VIEW
        d_data = gap_df[gap_df['District'] == sel_dist].iloc[0]
        with cols[0]: render_kpi("Food Available", f"{d_data['Total_Fodder_Tons']:.2f} T")
        with cols[1]: render_kpi("Food Needed", f"{d_data['Total_Demand_Tons']:.2f} T")
        with cols[2]: render_kpi("Difference", f"{d_data['Balance_Tons']:.0f} T")
        with cols[3]: render_kpi("Status", d_data['Status'])
        
        if d_data['Balance_Tons'] < 0:
            st.error(f"🚨 **Critical Shortage:** {sel_dist} is exhibiting a significant fodder deficit.")
        main_score = (d_data['Total_Fodder_Tons'] / d_data['Total_Demand_Tons'] * 100) if d_data['Total_Demand_Tons'] > 0 else 0
    else:
        # STATE VIEW
        with cols[0]: render_kpi("Food Available", f"{tot_state_supply/1e6:.2f}M T")
        with cols[1]: render_kpi("Food Needed", f"{tot_state_demand/1e6:.2f}M T")
        with cols[2]: render_kpi("Gap", f"{(tot_state_supply-tot_state_demand)/1e6:.2f}M T")
        with cols[3]: render_kpi("Red Districts", f"{len(gap_df[gap_df['Status']=='DEFICIT'])} Areas")
        st.info("✨ **Decision Signal:** Heuristic analysis indicates a potential supply-demand imbalance.")
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
            font=dict(size=12),
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
            number = {'suffix': "%", 'font': {'size': 60, 'color': '#0f172a'}},
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

# --- FOOTER ---
st.markdown("---")
st.markdown("© 2026 Department of Animal Husbandry | Build: 2.0.4")
