import streamlit as st
import pandas as pd
from database.alert_manager import resolve_alert


def show_alerts_page(alerts):

    st.title("🚨 Enterprise Security Alerts")

    st.caption("Monitor, investigate and manage security alerts.")

    st.markdown("---")

    total = len(alerts)

    critical = len(alerts[alerts["risk"] == "Critical"])

    high = len(alerts[alerts["risk"] == "High"])

    open_alerts = len(alerts[alerts["status"] == "Open"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Alerts", total)

    c2.metric("Critical", critical)

    c3.metric("High", high)

    c4.metric("Open", open_alerts)

    st.markdown("---")
    search = st.text_input(
        "🔍 Search Alert"
    )

    risk = st.selectbox(
        "Filter by Risk",
        [
            "All",
            "Critical",
            "High",
            "Medium",
            "Low"
        ]
    )

    data = alerts.copy()

    if search:

        data = data[
            data["threat"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if risk != "All":

        data = data[
            data["risk"] == risk
        ]
    st.subheader("🚨 Alert Queue")

    if data.empty:

        st.success("No alerts found.")

    else:

        for i, row in data.iterrows():

            with st.expander(
                f"{row['threat']} | {row['risk']}"
            ):

                st.write(
                    f"**Status:** {row['status']}"
                )

                st.write(
                    f"**Recommendation:** {row['recommendation']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    
                    if st.button(

                         "✅ Resolve",

                        key=f"resolve_{row['alert_id']}"

                    ):

                        with st.spinner("Resolving Alert..."):

                             resolve_alert(

                                 row["alert_id"]

                            )

                        st.toast(

                            "Alert Resolved Successfully",

                            icon="✅"

                        )
                        st.cache_data.clear()
                        st.rerun()
                with col2:

                    if st.button(
                        "📄 View Details",
                        key=f"details_{row['alert_id']}"
                    ):

                        st.info(f"""
### Alert Information

**Alert ID:** {row['alert_id']}

**Threat:** {row['threat']}

**Risk Level:** {row['risk']}

**Status:** {row['status']}

**Recommendation:**
{row['recommendation']}
""")
    st.markdown("---")

    st.subheader("📋 All Alerts")

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )