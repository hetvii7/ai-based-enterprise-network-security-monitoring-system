import streamlit as st
import pandas as pd
from pathlib import Path
from reports.report_generator import generate_report


def show_report_page(
    devices,
    logs,
    alerts,
    health
):

    st.title("📊 Enterprise Reports")

    st.caption(
        "Generate Executive Security Reports"
    )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Devices",
        len(devices)
    )

    c2.metric(
        "Security Logs",
        len(logs)
    )

    c3.metric(
        "Alerts",
        len(alerts)
    )

    if not health.empty:

        c4.metric(
            "Security Score",
            f"{int(health.iloc[0]['security_score'])}%"
        )

    else:

        c4.metric(
            "Security Score",
            "--"
        )

    st.markdown("---")
    st.subheader("📋 Executive Security Summary")

    st.info(
        f"""
Enterprise infrastructure currently contains **{len(devices)} devices**.

A total of **{len(logs)} security events** have been recorded.

There are currently **{len(alerts)} active alerts**.

The Enterprise Security Score is **{int(health.iloc[0]['security_score']) if not health.empty else '--'}%**.

The infrastructure is continuously monitored through the Enterprise SOC Dashboard.
"""
    )

    st.markdown("---")
    st.subheader("📥 Export Data")

    left, right = st.columns(2)

    with left:

        csv_logs = logs.to_csv(index=False)

        st.download_button(

            "⬇ Download Security Logs",

            csv_logs,

            "security_logs.csv",

            "text/csv",

            use_container_width=True

        )

    with right:

        csv_devices = devices.to_csv(index=False)

        st.download_button(

            "⬇ Download Device Inventory",

            csv_devices,

            "devices.csv",

            "text/csv",

            use_container_width=True

        )

    st.markdown("---")
    st.subheader("📄 Generate Executive PDF Report")

    if st.button(

        "Generate Enterprise Report",

        use_container_width=True

    ):

        try:

            report = generate_report()

            if report and Path(report).exists():

                st.success(

                    "Report Generated Successfully"

                )

                with open(report, "rb") as pdf:

                    st.download_button(

                        "⬇ Download Enterprise Report",

                        pdf,

                        "Enterprise_SOC_Report.pdf",

                        "application/pdf",

                        use_container_width=True

                    )

            else:

                st.error(

                    "Report generation failed."

                )

        except Exception as e:

            st.error(e)

    st.markdown("---")
    st.subheader("🛡 Security Assessment")

    if alerts.empty:

        st.success(
            "Enterprise Network Secure"
        )

    else:

        critical = len(

            alerts[
                alerts["risk"] == "Critical"
            ]

        )

        high = len(

            alerts[
                alerts["risk"] == "High"
            ]

        )

        st.warning(

            f"""
Critical Alerts : {critical}

High Alerts : {high}

Continue monitoring Enterprise infrastructure.
"""
        )

    st.markdown("---")

    st.caption(

        "Enterprise SOC Dashboard | Internship Project"

    )
