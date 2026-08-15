import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from database.database_manager import get_connection
from event_generator.generate_events import generate_event

# ===========================
# IMPORT PAGES
# ===========================

from utils.dashboard_page import show_dashboard
from utils.network_page import show_network_page
from utils.device_page import show_device_page
from utils.logs_page import show_logs_page
from utils.alerts_page import show_alerts_page
from utils.ai_page import show_ai_page
from utils.report_page import show_report_page

# ===========================
# PAGE CONFIG
# ===========================

st.set_page_config(

    page_title="Enterprise SOC Dashboard",

    page_icon="🛡",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ===========================
# AUTO REFRESH
# ===========================

st_autorefresh(

    interval=5000,

    key="refresh"

)

# ===========================
# LOAD CSS
# ===========================

css = Path("assets/style.css")

if css.exists():

    with open(css, encoding="utf-8") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True

        )
        
components.html(
    """
    <style>
    body{
        margin:0;
        overflow:hidden;
    }

    #cursor-glow{
        position:fixed;
        width:250px;
        height:250px;
        border-radius:50%;
        pointer-events:none;
        transform:translate(-50%,-50%);
        background:radial-gradient(circle,
            rgba(0,183,255,.18),
            rgba(0,183,255,.08),
            transparent 70%);
        filter:blur(45px);
        z-index:999999;
    }
    </style>

    <div id="cursor-glow"></div>

    <script>
    const glow=document.getElementById("cursor-glow");

    document.addEventListener("mousemove",(e)=>{
        glow.style.left=e.clientX+"px";
        glow.style.top=e.clientY+"px";
    });
    </script>
    """,
    height=0,
)
# ===========================
# DATABASE
# ===========================
@st.cache_data(ttl=5)
def load_data():

    connection = get_connection()

    devices = pd.read_sql_query(
        "SELECT * FROM devices",
        connection
    )

    logs = pd.read_sql_query(
        "SELECT * FROM security_logs ORDER BY log_id DESC",
        connection
    )

    alerts = pd.read_sql_query(
        "SELECT * FROM alerts ORDER BY alert_id DESC",
        connection
    )

    services = pd.read_sql_query(
        "SELECT * FROM services",
        connection
    )

    health = pd.read_sql_query(
        "SELECT * FROM network_health",
        connection
    )

    connection.close()

    return devices, logs, alerts, services, health

devices, logs, alerts, services, health = load_data()
# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("# 🛡 Enterprise SOC")

    st.caption(
        "AI Powered Security Platform"
    )

    st.markdown("---")

    page = st.radio(

        "Navigation",

        [

            "🏠 Dashboard",

            "🌐 Network",

            "💻 Devices",

            "📜 Security Logs",

            "🚨 Alerts",

            "🤖 AI Copilot",

            "📊 Reports"

        ],

        label_visibility="collapsed"

    )

    st.markdown("---")

    st.subheader("Enterprise Services")

    if services.empty:

        st.warning("No Services Found")

    else:

        for _, row in services.iterrows():

            if row["status"] == "Running":

                st.success(

                    f"🟢 {row['service_name']}"

                )

            else:

                st.error(

                    f"🔴 {row['service_name']}"

                )

    st.markdown("---")

    st.subheader("Quick Actions")

    if st.button(

        "⚡ Generate Demo Event",

        use_container_width=True

    ):

        with st.spinner("Generating Security Event..."):

            generate_event()

        st.toast(
        "Security Event Generated Successfully",
        icon="🛡"
    )

        st.rerun()
        

    st.markdown("---")

    st.info(

        "Enterprise SOC Dashboard\n\nInternship Project"

    )
# ==========================================================
# PAGE ROUTING
# ==========================================================

if page == "🏠 Dashboard":

    show_dashboard(

        devices=devices,

        logs=logs,

        alerts=alerts,

        services=services,

        health=health

    )

elif page == "🌐 Network":

    show_network_page(

        devices=devices,

        health=health

    )

elif page == "💻 Devices":

    show_device_page(

        devices=devices

    )

elif page == "📜 Security Logs":

    show_logs_page(

        logs=logs

    )

elif page == "🚨 Alerts":

    show_alerts_page(

        alerts=alerts

    )

elif page == "🤖 AI Copilot":

    show_ai_page(

        alerts=alerts,

        logs=logs

    )

elif page == "📊 Reports":

    show_report_page(

        devices=devices,

        logs=logs,

        alerts=alerts,

        health=health

    )
st.markdown("---")

st.caption(
    "Enterprise SOC Dashboard | Internship Project | Developed by Hetvi Upadhyay"
)