import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def show_dashboard(
    devices,
    logs,
    alerts,
    services,
    health
):

    # ==========================================================
    # HERO SECTION
    # ==========================================================

    time_now = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

    st.title("🛡 Enterprise SOC Dashboard")

    st.caption(
        "AI Powered Enterprise Security Operations Center"
    )

    st.markdown("---")

    hero1, hero2, hero3, hero4 = st.columns(4)

    with hero1:

        st.metric(

            "🏢 Organization",

            "Enterprise"

        )

    with hero2:

        st.metric(

            "🌐 Network",

            "Operational"

        )

    with hero3:

        st.metric(

            "🕒 Last Updated",

            time_now

        )

    with hero4:

        if not health.empty:

            st.metric(

                "🛡 Security Score",

                f"{int(health.iloc[0]['security_score'])}%"

            )

        else:

            st.metric(

                "🛡 Security Score",

                "--"

            )

    st.info(

        "Enterprise infrastructure is continuously monitored."

    )

    st.markdown("---")

    # ==========================================================
    # HEALTH
    # ==========================================================

    security_score = 0
    cpu_usage = 0
    memory_usage = 0

    if not health.empty:

        security_score = int(
            health.iloc[0]["security_score"]
        )

        cpu_usage = float(
            health.iloc[0]["cpu_usage"]
        )

        memory_usage = float(
            health.iloc[0]["memory_usage"]
        )

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "🖥 Devices",

            len(devices),

            "+2 Online"

        )

    with c2:

        st.metric(

            "📜 Security Logs",

            len(logs),

            "+15 Today"

        )

    with c3:

        st.metric(

            "🚨 Active Alerts",

            len(alerts),

            "+1 Critical"

        )

    with c4:

        st.metric(

            "🛡 Security Score",

            f"{security_score}%",

            "Healthy"

        )

    st.markdown("<br>", unsafe_allow_html=True)
    # ==========================================================
    # NETWORK HEALTH + SERVICES
    # ==========================================================

    left, right = st.columns([2, 1])

    with left:

        st.subheader("🌐 Enterprise Network Health")

        cpu_df = pd.DataFrame({

            "Metric": [

                "CPU Usage",

                "Memory Usage"

            ],

            "Usage": [

                cpu_usage,

                memory_usage

            ]

        })

        fig_cpu = px.bar(

            cpu_df,

            x="Metric",

            y="Usage",

            text="Usage",

            color="Metric",

            color_discrete_sequence=[

                "#00BFFF",

                "#38BDF8"

            ]

        )

        fig_cpu.update_traces(

            textposition="outside"

        )

        fig_cpu.update_layout(

            height=380,

            template="plotly_dark",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            showlegend=False,

            font=dict(

                color="white",

                size=14

            ),

            xaxis_title="",

            yaxis_title="Usage (%)",

            margin=dict(

                l=20,

                r=20,

                t=20,

                b=20

            )

        )

        st.plotly_chart(

            fig_cpu,

            use_container_width=True

        )

    with right:

        st.subheader("⚙ Enterprise Services")

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

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SECURITY ANALYTICS
    # ==========================================================

    chart1, chart2 = st.columns(2)

    with chart1:

        st.subheader("🚨 Threat Severity")

        if logs.empty:

            st.info("No Security Logs")

        else:

            severity = (

                logs["severity"]

                .value_counts()

                .reset_index()

            )

            severity.columns = [

                "Severity",

                "Count"

            ]

            fig = px.pie(

                severity,

                names="Severity",

                values="Count",

                hole=.60,

                color="Severity",

                color_discrete_map={

                    "Low": "#22C55E",

                    "Medium": "#FACC15",

                    "High": "#FB923C",

                    "Critical": "#EF4444"

                }

            )

            fig.update_layout(
                height=420,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="white",
                    size=14
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=40,
                    b=20
                ),
                legend=dict(
                    orientation="h",
                    y=-0.15,
                    x=0.5,
                    xanchor="center"
                )
            )
            
            fig.update_traces(
                textinfo="percent+label",
                textfont_size=14
            )

            st.plotly_chart(

                fig,

                use_container_width=True,
                config={"displayModeBar": False}

            )

    with chart2:

        st.subheader("📊 Top Security Events")

        if logs.empty:

            st.info("No Security Logs")

        else:

            events = (

                logs["event_type"]

                .value_counts()

                .head(8)

                .reset_index()

            )

            events.columns = [

                "Event",

                "Count"

            ]

            fig2 = px.bar(

                events,

                x="Event",

                y="Count",

                text="Count",

                color="Count",

                color_continuous_scale="Blues"

            )

            fig2.update_layout(
                height=420,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="white",
                    size=14
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=40,
                    b=20
                )
            )
            fig2.update_xaxes(
                tickangle=-35
            )

            fig2.update_traces(
                textposition="outside"
            )
            st.plotly_chart(

                fig2,

                use_container_width=True,
                config={"displayModeBar": False}

            )

    st.markdown("<br>", unsafe_allow_html=True)
    # ==========================================================
    # AI COPILOT + ACTIVE ALERTS
    # ==========================================================

    left, right = st.columns([2, 1])

    with left:

        st.subheader("🤖 AI Security Copilot")

        if alerts.empty:

            st.success("✅ No Active Threats Detected")

            st.info("Enterprise Network is Secure")

        else:

            latest = alerts.iloc[0]

            st.error(f"🚨 Current Threat : {latest['threat']}")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Risk Level",
                    latest["risk"]
                )

            with col2:

                st.metric(
                    "Status",
                    latest["status"]
                )

            st.markdown("### AI Recommendation")

            st.info(
                latest["recommendation"]
            )

            st.markdown("### Suggested Actions")

            st.write("✅ Verify related device logs")
            st.write("✅ Review firewall & ACL policies")
            st.write("✅ Check AAA authentication records")
            st.write("✅ Continue monitoring suspicious activity")

    with right:

        st.subheader("🚨 Active Alerts")

        if alerts.empty:

            st.success("No Active Alerts")

        else:

            for _, row in alerts.head(5).iterrows():

                if row["risk"] == "Critical":

                    st.error(
                        f"🚨 {row['threat']}"
                    )

                elif row["risk"] == "High":

                    st.warning(
                        f"⚠ {row['threat']}"
                    )

                else:

                    st.info(
                        f"ℹ {row['threat']}"
                    )

    st.markdown("---")

    # ==========================================================
    # DEVICE INVENTORY
    # ==========================================================

    st.subheader("💻 Enterprise Devices")

    st.dataframe(

        devices,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    # ==========================================================
    # RECENT SECURITY LOGS
    # ==========================================================

    st.subheader("📜 Recent Security Logs")

    st.dataframe(

        logs.head(20),

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    # ==========================================================
    # PDF REPORT
    # ==========================================================

    st.subheader("📄 Enterprise Security Report")

    try:

        from reports.report_generator import generate_report

        if st.button(

            "📄 Generate Security Report",

            use_container_width=True

        ):

            report_path = generate_report()

            if report_path:

                with open(report_path, "rb") as pdf:

                    st.success(
                        "Report Generated Successfully"
                    )

                    st.download_button(

                        "⬇ Download PDF Report",

                        pdf,

                        file_name="Enterprise_SOC_Report.pdf",

                        mime="application/pdf",

                        use_container_width=True

                    )

    except Exception as e:

        st.error(e)

    st.markdown("---")

    # ==========================================================
    # FOOTER
    # ==========================================================

    st.caption(

        "Enterprise SOC Dashboard | Internship Project | Developed using Python • SQLite • Streamlit • Plotly"

    )