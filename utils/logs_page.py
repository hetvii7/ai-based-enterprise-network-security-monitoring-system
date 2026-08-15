import streamlit as st
import pandas as pd
import plotly.express as px


def show_logs_page(logs):

    st.title("📜 Enterprise Security Logs")

    st.caption(
        "Live Security Event Monitoring"
    )

    st.markdown("---")

    total_logs = len(logs)

    critical = len(
        logs[
            logs["severity"] == "Critical"
        ]
    )

    high = len(
        logs[
            logs["severity"] == "High"
        ]
    )

    medium = len(
        logs[
            logs["severity"] == "Medium"
        ]
    )

    low = len(
        logs[
            logs["severity"] == "Low"
        ]
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Logs", total_logs)

    c2.metric("Critical", critical)

    c3.metric("High", high)

    c4.metric("Medium", medium)

    c5.metric("Low", low)

    st.markdown("---")
    left, middle, right = st.columns(3)

    with left:

        search = st.text_input(
            "🔍 Search Event"
        )

    with middle:

        severity = st.selectbox(

            "Severity",

            [

                "All",

                "Critical",

                "High",

                "Medium",

                "Low"

            ]

        )

    with right:

        action = st.selectbox(

            "Action",

            ["All"] +

            sorted(

                logs["action"]

                .unique()

                .tolist()

            )

        )

    filtered = logs.copy()

    if search:

        filtered = filtered[

            filtered["event_type"]

            .str.contains(

                search,

                case=False,

                na=False

            )

        ]

    if severity != "All":

        filtered = filtered[

            filtered["severity"]

            == severity

        ]

    if action != "All":

        filtered = filtered[

            filtered["action"]

            == action

        ]

    st.markdown("---")
    left, right = st.columns(2)

    with left:

        st.subheader("Threat Distribution")

        fig = px.pie(

            filtered,

            names="severity",

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

        st.subheader("Top Events")

        event_df = (

            filtered["event_type"]

            .value_counts()

            .reset_index()

        )

        event_df.columns = [

            "Event",

            "Count"

        ]

        fig2 = px.bar(

            event_df,

            x="Event",

            y="Count",

            text="Count",

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
    st.subheader("📋 Live Enterprise Logs")

    st.dataframe(

        filtered,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")
    st.subheader("🚨 Critical Events")

    critical_logs = filtered[

        filtered["severity"]

        == "Critical"

    ]

    if critical_logs.empty:

        st.success(

            "No Critical Security Events"

        )

    else:

        for _, row in critical_logs.iterrows():

            with st.expander(

                row["event_type"]

            ):

                st.write(

                    f"Source IP : {row['source_ip']}"

                )

                st.write(

                    f"Destination : {row['destination_ip']}"

                )

                st.write(

                    f"Action : {row['action']}"

                )

                st.write(

                    f"Timestamp : {row['timestamp']}"

                )
