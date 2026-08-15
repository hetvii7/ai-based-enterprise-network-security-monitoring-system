import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from pathlib import Path


def show_network_page(devices, health):

    st.title("🌐 Enterprise Network")

    st.caption(
        "Enterprise Network Infrastructure Monitoring"
    )

    st.markdown("---")

    # ======================================================
    # HERO
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "🖥 Devices",

            len(devices)

        )

    with c2:

        st.metric(

            "🌐 VLANs",

            "7"

        )

    with c3:

        st.metric(

            "🛡 Firewall",

            "Protected"

        )

    with c4:

        if not health.empty:

            st.metric(

                "Security",

                f"{int(health.iloc[0]['security_score'])}%"

            )

        else:

            st.metric(

                "Security",

                "--"

            )

    st.info(

        "Enterprise Network Status : Operational"

    )

    st.markdown("---")

    # ======================================================
    # NETWORK TOPOLOGY
    # ======================================================

    st.subheader("🗺 Enterprise Network Topology")

    st.info(
    "Packet Tracer network topology will be added in the final project."
        )

    st.markdown("---")
    
    # ======================================================
    # DEVICE STATUS
    # ======================================================

    st.subheader("💻 Enterprise Devices")

    search = st.text_input(

        "Search Device"

    )

    device_df = devices.copy()

    if search:

        device_df = device_df[

            device_df["hostname"]

            .str.contains(

                search,

                case=False,

                na=False

            )

        ]

    st.dataframe(

        device_df,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")
    # ======================================================
    # DEVICE TYPES
    # ======================================================

    left, right = st.columns(2)

    with left:

        st.subheader("📊 Device Types")

        fig = px.pie(

            devices,

            names="device_type",

            hole=.55,

            template="plotly_dark"

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
       
    with right:

        st.subheader("📍 Device Locations")

        fig2 = px.bar(

            devices,

            x="hostname",

            color="location",

            template="plotly_dark"

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

    st.markdown("---")
    # ======================================================
    # NETWORK SUMMARY
    # ======================================================

    st.subheader("📋 Network Summary")

    st.success(

        """
✅ Router Online

✅ Firewall Protected

✅ Core Switch Operational

✅ VLAN Communication Active

✅ DHCP Running

✅ DNS Running

✅ AAA Authentication Running

✅ Syslog Collecting Logs

✅ NTP Synchronized

Enterprise Network is operating normally.
"""
    )