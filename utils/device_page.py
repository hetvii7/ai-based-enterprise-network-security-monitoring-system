import streamlit as st
import pandas as pd
import plotly.express as px


def show_device_page(devices):

    st.title("💻 Enterprise Devices")

    st.caption(
        "Enterprise Device Inventory & Asset Monitoring"
    )

    st.markdown("---")

    total_devices = len(devices)

    online = len(
        devices[
            devices["status"] == "Online"
        ]
    )

    offline = len(
        devices[
            devices["status"] == "Offline"
        ]
    )

    device_types = devices["device_type"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🖥 Total Devices",
        total_devices
    )

    c2.metric(
        "🟢 Online",
        online
    )

    c3.metric(
        "🔴 Offline",
        offline
    )

    c4.metric(
        "⚙ Device Types",
        device_types
    )

    st.markdown("---")
    st.subheader("🔍 Search & Filters")

    left, right = st.columns(2)

    with left:

        search = st.text_input(
            "Search Hostname"
        )

    with right:

        device_type = st.selectbox(

            "Device Type",

            ["All"] +

            sorted(

                devices["device_type"]

                .unique()

                .tolist()

            )

        )

    filtered = devices.copy()

    if search:

        filtered = filtered[

            filtered["hostname"]

            .str.contains(

                search,

                case=False,

                na=False

            )

        ]

    if device_type != "All":

        filtered = filtered[

            filtered["device_type"]

            == device_type

        ]

    st.markdown("---")
    st.subheader("📋 Enterprise Inventory")

    st.dataframe(

        filtered,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")
    left, right = st.columns(2)

    with left:

        st.subheader("📊 Device Types")

        fig = px.pie(

            filtered,

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

            filtered,

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
    st.subheader("🖥 Device Details")

    for _, row in filtered.iterrows():

        with st.expander(

            f"{row['hostname']} ({row['device_type']})"

        ):

            st.write(

                f"**IP Address:** {row['ip_address']}"

            )

            st.write(

                f"**MAC Address:** {row['mac_address']}"

            )

            st.write(

                f"**Department ID:** {row['department_id']}"

            )

            st.write(

                f"**VLAN:** {row['vlan_id']}"

            )

            st.write(

                f"**Location:** {row['location']}"

            )

            if row["status"] == "Online":

                st.success("🟢 Device Online")

            else:

                st.error("🔴 Device Offline")