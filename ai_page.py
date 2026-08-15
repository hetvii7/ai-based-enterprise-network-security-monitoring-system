import streamlit as st
import pandas as pd
from datetime import datetime
from database.alert_manager import resolve_alert
from utils.ai_model import analyze_security_logs


def show_ai_page(alerts, logs):

    st.title("🤖 Enterprise AI Security Copilot")

    st.caption(
        "AI Powered Threat Analysis & Incident Response"
    )

    st.markdown("---")

    if alerts.empty:

        st.success("✅ No Active Security Threats")

        st.info(
            "AI Analysis: Enterprise network appears healthy."
        )

        return

    latest = alerts.iloc[0]

    threat = latest["threat"]
    risk = latest["risk"]
    recommendation = latest["recommendation"]
    status = latest["status"]

# ==========================================================
# MACHINE LEARNING ANALYSIS
# ==========================================================
    ml_result = analyze_security_logs(logs)
    
    ml_prediction = ml_result["prediction"]
    ml_confidence = ml_result["confidence"]
    anomaly_count = ml_result["anomaly_count"]
    
    confidence = ml_confidence
    
# ==========================================================
# METRICS
# ==========================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Threat",
            threat
        )

    with col2:

        st.metric(
            "Risk",
            risk
        )

    with col3:

        st.metric(
            "Status",
            status
        )

    with col4:

        st.metric(
            "AI Confidence",
            f"{confidence}%"
        )

    st.markdown("---")
    
    st.subheader("🤖 ML Security Analysis")

    if ml_prediction == "Anomalous Activity Detected":

        st.warning(
            f"⚠️ {ml_prediction}"
        )

    else:

        st.success(
            f"✅ {ml_prediction}"
        )

    st.write(
        f"Machine Learning detected **{anomaly_count} anomalous security events** "
        f"from the available security logs."
    )
    # ==========================================================
    # AI THREAT SUMMARY
    # ==========================================================

    st.subheader("🧠 AI Threat Summary")

    summary = ""

    mitre = ""

    if threat == "AAA Authentication Failure":

        summary = (
            "Multiple authentication failures indicate a possible "
            "brute-force attack against the AAA server. "
            "Immediate investigation is recommended."
        )

        mitre = "Credential Access (TA0006)"

    elif threat == "Port Scan Detected":

        summary = (
            "A reconnaissance scan has been detected. "
            "An attacker may be identifying open services before exploitation."
        )

        mitre = "Reconnaissance (TA0043)"

    elif threat == "ACL Denied":

        summary = (
            "Firewall or ACL successfully blocked unauthorized traffic. "
            "Review the source host for suspicious behaviour."
        )

        mitre = "Initial Access (TA0001)"

    elif threat == "Guest VLAN Access Attempt":

        summary = (
            "Guest VLAN isolation prevented unauthorized access. "
            "Network segmentation is functioning correctly."
        )

        mitre = "Defense Evasion (TA0005)"

    else:

        summary = (
            "Suspicious security activity detected. "
            "Further investigation is recommended."
        )

        mitre = "Unknown Technique"

    st.info(summary)

    st.markdown("### 🎯 MITRE ATT&CK Mapping")

    st.success(mitre)

    st.markdown("---")
    # ==========================================================
    # AI RECOMMENDATIONS
    # ==========================================================

    st.subheader("🤖 AI Recommended Actions")

    recommendations = []

    if threat == "AAA Authentication Failure":

        recommendations = [

            "Review AAA Server Logs",

            "Check Failed Login Attempts",

            "Verify User Credentials",

            "Enable Account Lockout Policy",

            "Monitor Authentication Events"

        ]

    elif threat == "Port Scan Detected":

        recommendations = [

            "Block Source IP",

            "Review Firewall Logs",

            "Enable IDS Monitoring",

            "Check Open Ports",

            "Monitor Network Traffic"

        ]

    elif threat == "ACL Denied":

        recommendations = [

            "Verify ACL Rules",

            "Review Firewall Policies",

            "Identify Source Device",

            "Check Network Segmentation"

        ]

    else:

        recommendations = [

            "Review Security Logs",

            "Investigate Device",

            "Continue Monitoring",

            "Escalate if Activity Continues"

        ]

    for item in recommendations:

        st.write(f"✅ {item}")

    st.markdown("---")
    # ==========================================================
    # AI INSIGHTS
    # ==========================================================

    left, right = st.columns(2)

    with left:

        st.subheader("📊 AI Threat Assessment")

        st.metric(

            "Confidence",

            f"{confidence}%"

        )

        st.metric(

            "Threat Level",

            risk

        )

    with right:

        st.subheader("📈 AI Incident Statistics")

        st.metric(

            "Total Security Logs",

            len(logs)

        )

        st.metric(

            "Open Alerts",

            len(alerts)

        )

    st.markdown("---")
