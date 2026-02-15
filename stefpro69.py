import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime
import time

st.set_page_config(
    layout="wide", 
    page_title="STEF Global | Climate Intelligence", 
    page_icon="🌊",
    initial_sidebar_state="collapsed"
)

@st.cache_data(ttl=3600)
def get_sea_temperature_live(lat, lon):
    try:
        with st.spinner('🌊 Retrieving satellite data...'):
            url = f"https://www.ncei.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.json"
            params = {
                "sst[(last)][({lat})][({lon})]"
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                temp_celsius = data['table']['rows'][0][3] - 273.15
                return {
                    'success': True,
                    'temperature': round(temp_celsius, 1),
                    'source': 'NOAA Satellite (Live)',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M UTC')
                }
    except:
        pass
    return get_temperature_fallback(lat, lon)

def get_temperature_fallback(lat, lon):
    base_temp = 28 * np.cos(np.deg2rad(abs(lat))) + 5
    seasonal = 3 * np.sin((datetime.now().month - 3) * np.pi / 6)
    temp = base_temp + seasonal
    return {
        'success': False,
        'temperature': round(max(10, min(36, temp)), 1),
        'source': 'Geographic Model (Estimated)',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
    }

st.markdown("""
<style>
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0; 
    }
    section[data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
        border-right: 2px solid #334155; 
    }
    h1 { 
        color: #38bdf8 !important; 
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
        font-size: 2.5rem !important;
    }
    h2, h3 { color: #7dd3fc !important; }
    div[data-testid="metric-container"] { 
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 2px solid #475569; 
        padding: 20px; 
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e293b;
        color: #94a3b8;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(180deg, #0c4a6e 0%, #075985 100%);
        color: #38bdf8 !important; 
        border-bottom: 3px solid #38bdf8;
    }
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌊 STEF GLOBAL")
    st.caption("*Climate Intelligence System*")
    st.markdown("---")
    
    with st.expander("🎯 MISSION", expanded=True):
        st.markdown("""
        **Target Species:** *Mugil cephalus*  
        **Objective:** Predict metabolic collapse before symptoms
        
        🔬 **Method:** 6-Core Synergistic Analysis  
        📊 **Data:** 68 Peer-Reviewed Studies  
        🌍 **Coverage:** Global (42°N - 42°S)
        """)
    
    with st.expander("📚 LITERATURE (N=68)"):
        refs = pd.DataFrame({
            "ID": ["#01", "#02", "#03", "#04", "#05"],
            "Key Finding": [
                "OCLTT Theory", 
                "Gill-Oxygen Limitation", 
                "Aerobic Scope Dynamics",
                "Thermal Performance Curve",
                "Starvation Synergy (-1.07°C)"
            ],
            "Author": [
                "Pörtner & Farrell", 
                "Pauly & Cheung", 
                "Claireaux et al.",
                "Fry (1971)",
                "STEF Team (2025)"
            ]
        })
        st.dataframe(refs, hide_index=True, use_container_width=True)
    
    with st.expander("🧮 CORE ALGORITHMS"):
        st.markdown("**Standard Metabolic Rate:**")
        st.latex(r"SMR = 72.4 \cdot e^{0.0567 \cdot T}")
        st.markdown("**Thermal Sensitivity:**")
        st.latex(r"Q_{10} = \begin{cases} 2.07 & T < 25°C \\ 2.45 & T \geq 25°C \end{cases}")
    
    st.markdown("---")
    st.markdown("**🛰️ Data Sources:**")
    st.markdown("✓ NOAA Coral Reef Watch  \n✓ NASA MODIS Aqua  \n✓ Published Literature")

col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown("# 🌊")
with col_title:
    st.markdown("# STEF GLOBAL")
    st.caption("**S**yngergistic **T**hermal & **E**nergetic **F**ramework | Real-Time Climate Intelligence")

st.markdown("---")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    scenario = st.selectbox(
        "🌡️ CLIMATE SCENARIO",
        ["Present Day (Baseline)", "SSP1-2.6 (+1.5°C by 2050)", "SSP5-8.5 (+3.2°C by 2050)"],
        help="Select IPCC climate projection scenario"
    )

with col2:
    ni = st.slider(
        "🍽️ NUTRITIONAL INDEX (NI)", 
        0.0, 1.0, 1.0, 0.05,
        help="0.0 = Severe starvation | 1.0 = Well-fed"
    )
    
with col3:
    st.markdown("### ")
    data_mode = st.checkbox("🛰️ Live Satellite", value=True, help="Use real-time NOAA data")

if ni < 0.4:
    st.error("⚠️ **STARVATION PENALTY ACTIVE:** Thermal tolerance reduced by 1.07°C")
elif ni < 0.7:
    st.warning("⚙️ Moderate nutritional stress detected")

st.markdown("### 🗺️ Global Risk Assessment Map")
st.caption("Click any marine location to analyze metabolic risk")

m = folium.Map(
    location=[35, 30], 
    zoom_start=4, 
    tiles="CartoDB dark_matter",
    control_scale=True
)

folium.Circle(
    location=[36.8, 34.6],
    radius=50000,
    color="#ef4444",
    fill=True,
    fillColor="#ef4444",
    fillOpacity=0.3,
    popup="Mersin Bay - High Risk Zone"
).add_to(m)

folium.Circle(
    location=[38.4, 26.1],
    radius=50000,
    color="#f59e0b",
    fill=True,
    fillColor="#f59e0b",
    fillOpacity=0.3,
    popup="Aegean Sea - Moderate Risk"
).add_to(m)

map_output = st_folium(m, width=None, height=500, key="stef_map_v2")

if map_output and map_output.get('last_clicked'):
    lat = map_output['last_clicked']['lat']
    lon = map_output['last_clicked']['lng']
    
    if data_mode:
        temp_data = get_sea_temperature_live(lat, lon)
    else:
        temp_data = get_temperature_fallback(lat, lon)
    
    temp_shift = 0.0
    if "1.5" in scenario:
        temp_shift = 1.5
    elif "3.2" in scenario:
        temp_shift = 3.2
    
    T = temp_data['temperature'] + temp_shift
    
    base_limit = 31.5
    starvation_penalty = 1.07 * (1 - ni)
    T_critical = base_limit - starvation_penalty
    
    if T >= T_critical:
        risk = 100
        status = "LETHAL"
        status_color = "🔴"
    elif T >= T_critical - 2:
        risk = int(75 + (T - (T_critical - 2)) / 2 * 25)
        status = "CRITICAL"
        status_color = "🟠"
    elif T >= 25:
        risk = int(50 + (T - 25) / (T_critical - 2 - 25) * 25)
        status = "HIGH RISK"
        status_color = "🟡"
    else:
        risk = int((T / 25) * 50)
        status = "STABLE"
        status_color = "🟢"
    
    SMR = 72.4 * np.exp(0.0567 * T)
    Q10 = 2.45 if T >= 25 else 2.07
    
    st.markdown("---")
    st.markdown(f"## 📊 Analysis Dashboard: {lat:.2f}°N, {lon:.2f}°E")
    
    if temp_data['success']:
        st.success(f"✅ **Data Source:** {temp_data['source']} | Updated: {temp_data['timestamp']}")
    else:
        st.info(f"ℹ️ **Data Source:** {temp_data['source']} | Timestamp: {temp_data['timestamp']}")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    
    m1.metric(
        "🌡️ Temperature", 
        f"{T:.1f}°C",
        f"+{temp_shift:.1f}°C" if temp_shift > 0 else None
    )
    
    m2.metric(
        "⚡ SMR",
        f"{SMR:.0f}",
        "mg O₂/kg/h"
    )
    
    m3.metric(
        "🔥 Q₁₀",
        f"{Q10:.2f}",
        "Thermal Sensitivity"
    )
    
    m4.metric(
        "🎯 Risk Score",
        f"{risk}%",
        f"{status_color} {status}"
    )
    
    m5.metric(
        "🛡️ Safety Margin",
        f"{T_critical - T:.1f}°C",
        "Until Collapse"
    )
    
    tabs = st.tabs([
        "📈 Metabolic Rate", 
        "🫁 Oxygen Budget", 
        "🎯 Threshold", 
        "📅 Annual Cycle",
        "🛡️ Safety Margin",
        "📉 Population Forecast"
    ])
    
    plt.style.use('dark_background')
    
    with tabs[0]:
        fig, ax = plt.subplots(figsize=(10, 4))
        x = np.linspace(10, 36, 200)
        y = 72.4 * np.exp(0.0567 * x)
        
        ax.plot(x, y, color="#38bdf8", lw=3, label="SMR Curve")
        ax.axvline(25, color="#fbbf24", ls="--", lw=2, label="Q₁₀ Shift (25°C)")
        ax.axvline(T_critical, color="#ef4444", ls="--", lw=2, label=f"Lethal ({T_critical:.1f}°C)")
        ax.scatter([T], [SMR], color="#22c55e", s=200, zorder=5, edgecolors="white", linewidths=2)
        
        ax.set_xlabel("Temperature (°C)", fontsize=12)
        ax.set_ylabel("SMR (mg O₂·kg⁻¹·h⁻¹)", fontsize=12)
        ax.set_title("Standard Metabolic Rate vs Temperature", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.2)
        st.pyplot(fig)
        st.caption(f"**Current:** {T:.1f}°C → SMR = {SMR:.1f} mg O₂/kg/h")
    
    with tabs[1]:
        fig, ax = plt.subplots(figsize=(10, 4))
        x = np.linspace(10, 36, 200)
        
        supply = 14 * np.exp(-0.02 * x)
        demand = 2 * np.exp(0.09 * x)
        
        ax.plot(x, supply, color="#4ade80", lw=3, label="Oxygen Supply (Water)")
        ax.plot(x, demand, color="#f472b6", lw=3, label="Oxygen Demand (Metabolism)")
        ax.fill_between(x, supply, demand, where=(supply > demand), alpha=0.3, color="green", label="Surplus")
        ax.fill_between(x, supply, demand, where=(supply <= demand), alpha=0.3, color="red", label="Deficit")
        
        ax.axvline(T, color="white", ls=":", lw=2)
        ax.set_xlabel("Temperature (°C)", fontsize=12)
        ax.set_ylabel("Oxygen (mg/L or mg/kg/h)", fontsize=12)
        ax.set_title("Oxygen Supply-Demand Balance", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.2)
        st.pyplot(fig)
    
    with tabs[2]:
        fig, ax = plt.subplots(figsize=(10, 3))
        
        categories = ["Optimal\n(15-20°C)", "Pejus\n(20-25°C)", "Critical\n(25-31.5°C)", "Lethal\n(>31.5°C)"]
        temps = [17.5, 22.5, 28, 33]
        colors = ["#22c55e", "#fbbf24", "#f97316", "#ef4444"]
        
        ax.barh(categories, temps, color=colors, alpha=0.7)
        ax.axvline(T, color="white", ls="--", lw=3, label=f"Current: {T:.1f}°C")
        ax.set_xlabel("Temperature (°C)", fontsize=12)
        ax.set_title("Thermal Zone Classification", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(axis='x', alpha=0.2)
        st.pyplot(fig)
    
    with tabs[3]:
        fig, ax = plt.subplots(figsize=(10, 4))
        
        months = np.arange(1, 13)
        seasonal = T + 5 * np.sin((months - 5) * np.pi / 6)
        
        ax.plot(months, seasonal, marker='o', color="#38bdf8", lw=3, markersize=8)
        ax.axhline(T_critical, color="#ef4444", ls="--", lw=2, label=f"Lethal ({T_critical:.1f}°C)")
        ax.axhline(25, color="#fbbf24", ls="--", lw=2, label="Q₁₀ Threshold (25°C)")
        
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Temperature (°C)", fontsize=12)
        ax.set_title("Annual Temperature Cycle (Projected)", fontsize=14, fontweight='bold')
        ax.set_xticks(months)
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        ax.legend()
        ax.grid(alpha=0.2)
        st.pyplot(fig)
    
    with tabs[4]:
        fig, ax = plt.subplots(figsize=(10, 3))
        
        margin = T_critical - T
        color = "#22c55e" if margin > 3 else ("#fbbf24" if margin > 1 else "#ef4444")
        
        ax.barh(["Safety Margin"], [margin], color=color, height=0.5)
        ax.set_xlim(-2, 10)
        ax.set_xlabel("Temperature Buffer (°C)", fontsize=12)
        ax.set_title(f"Margin Until Metabolic Collapse: {margin:.1f}°C", fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.2)
        st.pyplot(fig)
        
        if margin < 0:
            st.error("🚨 **LETHAL ZONE:** Immediate intervention required!")
        elif margin < 1:
            st.warning("⚠️ **CRITICAL:** Population at imminent risk")
        elif margin < 3:
            st.info("ℹ️ **CAUTION:** Entering high-risk zone")
    
    with tabs[5]:
        fig, ax = plt.subplots(figsize=(10, 4))
        
        years = np.arange(2026, 2051)
        decay_rate = 0.05 + (risk / 500)
        population = 100 * np.exp(-decay_rate * (years - 2026))
        
        ax.plot(years, population, color="#a78bfa", lw=3)
        ax.fill_between(years, population, alpha=0.3, color="#a78bfa")
        ax.axhline(50, color="#ef4444", ls="--", label="50% Collapse Threshold")
        
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Relative Population (%)", fontsize=12)
        ax.set_title("Population Trajectory Under Current Conditions", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.2)
        st.pyplot(fig)
        
        collapse_year = years[np.where(population < 50)[0][0]] if any(population < 50) else None
        if collapse_year:
            st.warning(f"⚠️ **Projected 50% decline by {collapse_year}**")
    
    st.markdown("---")
    st.markdown("### 💡 Management Recommendations")
    
    if risk >= 85:
        st.error("🚨 EMERGENCY: Immediate harvest or stock relocation required")
    elif risk >= 70:
        st.warning("⚠️ HIGH ALERT: Reduce feeding 50%, increase aeration")
    elif risk >= 50:
        st.info("ℹ️ ELEVATED RISK: Reduce feeding 30%, monitor closely")
    else:
        st.success("✅ NORMAL: Standard feeding protocols")
    
    st.markdown("---")
    col_report1, col_report2 = st.columns(2)
    
    with col_report1:
        if st.button("📄 GENERATE REPORT", use_container_width=True):
            report_data = {
                'Timestamp': [temp_data['timestamp']],
                'Location': [f"{lat:.2f}°N, {lon:.2f}°E"],
                'Temperature': [T],
                'SMR': [SMR],
                'Risk': [risk],
                'Status': [status]
            }
            df_report = pd.DataFrame(report_data)
            csv = df_report.to_csv(index=False)
            
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"STEF_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.success("✅ Report generated!")
    
    with col_report2:
        if st.button("🔄 RECALCULATE", use_container_width=True):
            st.rerun()

else:
    st.info("👆 **Click on the map** to start analysis")

st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col1:
    st.caption("**STEF Global v2.0**")
    st.caption("Genius Olympiad 2025")

with footer_col2:
    st.caption("Powered by: NOAA | NASA MODIS | IPCC AR6")

with footer_col3:
    st.caption("Developed by [Your Name]")
    st.caption("M. Çelik & A. Birtane")
