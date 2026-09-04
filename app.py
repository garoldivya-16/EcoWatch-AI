import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="EcoWatch AI",
    page_icon="🌍",
    layout="wide"
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_csv(
    "processed_waste_data.csv"
)

    return df


df = load_data()


# ==========================================
# WEBSITE HEADER
# ==========================================

st.title("🌍 EcoWatch AI")

st.subheader(
    "Smart Waste, Pollution & Environmental Compliance Management System"
)

st.divider()


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🌍 EcoWatch AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard Overview",
        "🗺️ Risk Map",
        "🚨 Smart Alerts",
        "🤖 Recommendations",
        "🏆 Zone Performance",
        "📋 Data Explorer"
    ]
)

st.sidebar.divider()

st.sidebar.header("🔍 Dashboard Filters")

# Zone filter
zones = sorted(df["collection_zone"].unique())

selected_zones = st.sidebar.multiselect(
    "Select Collection Zone",
    options=zones,
    default=zones
)


# District filter
districts = sorted(df["district"].unique())

selected_districts = st.sidebar.multiselect(
    "Select District",
    options=districts,
    default=districts
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df[
    (df["collection_zone"].isin(selected_zones))
    &
    (df["district"].isin(selected_districts))
]


# ==========================================
# KPI CALCULATIONS
# ==========================================

total_waste = filtered_df["waste_weight_kg"].sum()

average_aqi = filtered_df["air_quality_index"].mean()

critical_areas = len(
    filtered_df[
        filtered_df["waste_risk_level"] == "Critical"
    ]
)

violations = len(
    filtered_df[
        filtered_df["compliance_status"] == "Violation"
    ]
)
# ==========================================
# GLOBAL CALCULATIONS
# ==========================================

total_waste = filtered_df["waste_weight_kg"].sum()

average_aqi = filtered_df["air_quality_index"].mean()

critical_areas = len(
    filtered_df[
        filtered_df["waste_risk_level"] == "Critical"
    ]
)

violations = len(
    filtered_df[
        filtered_df["compliance_status"] == "Violation"
    ]
)

# ==========================================
# GLOBAL ALERT CALCULATIONS
# ==========================================

critical_waste_alerts = filtered_df[
    filtered_df["waste_risk_level"] == "Critical"
]

critical_pollution_alerts = filtered_df[
    filtered_df["pollution_risk_level"] == "Critical"
]

violation_alerts = filtered_df[
    filtered_df["compliance_status"] == "Violation"
]

if page == "📊 Dashboard Overview":
    # ==========================================
    # HERO SECTION
    # ==========================================

    st.markdown(
        """
        <div style="
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 25px;
        ">
            <h1>🌍 EcoWatch AI</h1>
            <h3>
                Smart Waste, Pollution & Environmental
                Compliance Management System
            </h3>
            <p style="font-size:18px;">
                Monitor environmental conditions, identify
                high-risk areas, generate smart alerts, and
                support data-driven waste management decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ------------------------------------------
    # KEY FEATURES
    # ------------------------------------------

    feature1, feature2, feature3, feature4 = st.columns(4)

    feature1.info(
        "♻️ **Smart Waste Monitoring**\n\n"
        "Track waste generation, bin levels and collection activity."
    )

    feature2.info(
        "🌫️ **Pollution Monitoring**\n\n"
        "Analyze AQI and identify pollution risk levels."
    )

    feature3.info(
        "🚨 **Compliance Monitoring**\n\n"
        "Detect environmental warnings and violations."
    )

    feature4.info(
        "🤖 **AI-Based Decisions**\n\n"
        "Recommend recycling, composting and energy recovery."
    )

    st.divider()

    # ==========================================
    # KPI CARDS
    # ==========================================

    st.markdown("## 📊 Environmental Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "♻️ Total Waste Collected",
        f"{total_waste:,.0f} kg"
    )

    col2.metric(
        "🌫️ Average AQI",
        f"{average_aqi:.1f}"
    )

    col3.metric(
        "🔴 Critical Risk Areas",
        critical_areas
    )

    col4.metric(
        "⚠️ Compliance Violations",
        violations
    )

# ==========================================
# CHARTS
# ==========================================

st.divider()

st.markdown("## 📈 Waste & Pollution Analysis")

col1, col2 = st.columns(2)
# ------------------------------------------
# CHART 1: TOTAL WASTE BY COLLECTION ZONE
# ------------------------------------------

waste_by_zone = (
    filtered_df
    .groupby("collection_zone")["waste_weight_kg"]
    .sum()
    .reset_index()
)

fig_waste = px.bar(
    waste_by_zone,
    x="collection_zone",
    y="waste_weight_kg",
    title="Total Waste Collected by Zone",
    labels={
        "collection_zone": "Collection Zone",
        "waste_weight_kg": "Total Waste (kg)"
    }
)

col1.plotly_chart(
    fig_waste,
    width="stretch"
)


# ------------------------------------------
# CHART 2: POLLUTION RISK DISTRIBUTION
# ------------------------------------------

pollution_risk = (
    filtered_df["pollution_risk_level"]
    .value_counts()
    .reset_index()
)

pollution_risk.columns = [
    "Pollution Risk Level",
    "Number of Records"
]

fig_pollution = px.pie(
    pollution_risk,
    names="Pollution Risk Level",
    values="Number of Records",
    title="Pollution Risk Distribution"
)

col2.plotly_chart(
    fig_pollution,
    width="stretch"
)
# ==========================================
# RISK & COMPLIANCE ANALYSIS
# ==========================================

st.divider()

st.markdown("## ⚠️ Risk & Compliance Analysis")

col3, col4 = st.columns(2)


# ------------------------------------------
# CHART 3: WASTE RISK DISTRIBUTION
# ------------------------------------------

waste_risk = (
    filtered_df["waste_risk_level"]
    .value_counts()
    .reset_index()
)

waste_risk.columns = [
    "Waste Risk Level",
    "Number of Records"
]

fig_waste_risk = px.bar(
    waste_risk,
    x="Waste Risk Level",
    y="Number of Records",
    title="Waste Risk Level Distribution",
    category_orders={
        "Waste Risk Level":
        ["Low", "Medium", "High", "Critical"]
    }
)

col3.plotly_chart(
    fig_waste_risk,
    width="stretch"
)


# ------------------------------------------
# CHART 4: COMPLIANCE STATUS
# ------------------------------------------

compliance_data = (
    filtered_df["compliance_status"]
    .value_counts()
    .reset_index()
)

compliance_data.columns = [
    "Compliance Status",
    "Number of Records"
]

fig_compliance = px.pie(
    compliance_data,
    names="Compliance Status",
    values="Number of Records",
    title="Environmental Compliance Status"
)

col4.plotly_chart(
    fig_compliance,
    width="stretch"
)

if page == "🗺️ Risk Map":

    # ==========================================
    # GEOGRAPHICAL RISK MAP
    # ==========================================

    st.divider()

    st.markdown("## 🗺️ Waste & Pollution Risk Map")

    map_df = filtered_df[
        [
            "latitude",
            "longitude",
            "collection_zone",
            "district",
            "waste_risk_level",
            "pollution_risk_level",
            "compliance_status",
            "waste_weight_kg",
            "air_quality_index"
        ]
    ].copy()

    fig_map = px.scatter_map(
        map_df,
        lat="latitude",
        lon="longitude",
        hover_name="collection_zone",
        hover_data={
            "district": True,
            "waste_risk_level": True,
            "pollution_risk_level": True,
            "compliance_status": True,
            "waste_weight_kg": True,
            "air_quality_index": True,
            "latitude": False,
            "longitude": False
        },
        color="pollution_risk_level",
        zoom=4,
        height=550,
        title="Geographical Distribution of Pollution Risk"
    )

    st.plotly_chart(
        fig_map,
        width="stretch"
    )
if page == "🚨 Smart Alerts":

    # ==========================================
    # SMART ALERT SYSTEM
    # ==========================================

    st.divider()

    st.markdown("## 🚨 Smart Environmental Alerts")

    # Critical waste risk alerts
    critical_waste_alerts = filtered_df[
        filtered_df["waste_risk_level"] == "Critical"
    ]

    # Critical pollution risk alerts
    critical_pollution_alerts = filtered_df[
        filtered_df["pollution_risk_level"] == "Critical"
    ]

    # Compliance violation alerts
    violation_alerts = filtered_df[
        filtered_df["compliance_status"] == "Violation"
    ]


    # Alert summary
    alert_col1, alert_col2, alert_col3 = st.columns(3)

    alert_col1.metric(
        "🔴 Critical Waste Alerts",
        len(critical_waste_alerts)
    )

    alert_col2.metric(
        "🌫️ Critical Pollution Alerts",
        len(critical_pollution_alerts)
    )

    alert_col3.metric(
        "🚨 Compliance Violations",
        len(violation_alerts)
    )


    # High priority alerts
    st.markdown("### ⚠️ High Priority Locations Requiring Attention")

    high_priority_alerts = filtered_df[
        (
            (filtered_df["waste_risk_level"] == "Critical")
            |
            (filtered_df["pollution_risk_level"] == "Critical")
            |
            (filtered_df["compliance_status"] == "Violation")
        )
    ]


    if len(high_priority_alerts) > 0:

        st.dataframe(
            high_priority_alerts[
                [
                    "record_id",
                    "collection_zone",
                    "district",
                    "waste_category",
                    "bin_fill_level_pct",
                    "air_quality_index",
                    "carbon_emission_kg",
                    "waste_risk_level",
                    "pollution_risk_level",
                    "compliance_status"
                ]
            ],
            width="stretch"
        )

    else:

        st.success(
            "No critical environmental alerts found for the selected filters."
        )
if page == "🤖 Recommendations":
# ==========================================
# SMART MANAGEMENT RECOMMENDATIONS
# ==========================================

     st.divider()

st.markdown("## 🤖 Smart Management Recommendations")


# ------------------------------------------
# CALCULATE AVERAGE SCORES
# ------------------------------------------

avg_recycling = filtered_df[
    "recycling_feasibility_score"
].mean()

avg_compost = filtered_df[
    "compost_quality_score"
].mean()

avg_energy = filtered_df[
    "energy_recovery_score"
].mean()

avg_resource_recovery = filtered_df[
    "resource_recovery_score"
].mean()


# ------------------------------------------
# RECOMMENDATION KPI CARDS
# ------------------------------------------

rec_col1, rec_col2, rec_col3, rec_col4 = st.columns(4)

rec_col1.metric(
    "♻️ Recycling Potential",
    f"{avg_recycling:.1f}/100"
)

rec_col2.metric(
    "🌱 Compost Potential",
    f"{avg_compost:.1f}/100"
)

rec_col3.metric(
    "⚡ Energy Recovery",
    f"{avg_energy:.1f}/100"
)

rec_col4.metric(
    "🔄 Resource Recovery",
    f"{avg_resource_recovery:.1f}/100"
)


# ------------------------------------------
# MANAGEMENT DECISION DISTRIBUTION
# ------------------------------------------

st.markdown("### 📊 Recommended Management Actions")

decision_data = (
    filtered_df["management_decision"]
    .value_counts()
    .reset_index()
)

decision_data.columns = [
    "Management Decision",
    "Number of Records"
]


fig_decision = px.bar(
    decision_data,
    x="Management Decision",
    y="Number of Records",
    title="AI-Based Waste Management Recommendations",
    labels={
        "Management Decision":
        "Recommended Action",

        "Number of Records":
        "Number of Locations"
    }
)

st.plotly_chart(
    fig_decision,
    width="stretch"
)


# ------------------------------------------
# TOP RECOMMENDED ACTION
# ------------------------------------------

top_decision = (
    filtered_df["management_decision"]
    .mode()[0]
)

st.info(
    f"🤖 Smart Recommendation: "
    f"The most suitable management action for the "
    f"currently selected data is **{top_decision}**."
)
# ==========================================
# ENVIRONMENTAL HEALTH SCORE
# ==========================================

st.divider()

st.markdown("## 🌍 Environmental Health Score")


# ------------------------------------------
# CALCULATE ENVIRONMENTAL INDICATORS
# ------------------------------------------

avg_bin_fill = filtered_df["bin_fill_level_pct"].mean()

avg_carbon = filtered_df["carbon_emission_kg"].mean()

violation_percentage = (
    len(violation_alerts) / len(filtered_df)
) * 100

critical_pollution_percentage = (
    len(critical_pollution_alerts) / len(filtered_df)
) * 100


# ------------------------------------------
# NORMALIZE VALUES
# ------------------------------------------

aqi_score = max(
    0,
    100 - (average_aqi / 5)
)

bin_score = max(
    0,
    100 - avg_bin_fill
)

carbon_score = max(
    0,
    100 - ((avg_carbon / 120) * 100)
)

compliance_score = max(
    0,
    100 - violation_percentage
)

pollution_score = max(
    0,
    100 - critical_pollution_percentage
)


# ------------------------------------------
# FINAL ENVIRONMENTAL HEALTH SCORE
# ------------------------------------------

environmental_health_score = (
    aqi_score * 0.30
    +
    bin_score * 0.20
    +
    carbon_score * 0.20
    +
    compliance_score * 0.15
    +
    pollution_score * 0.15
)


# ------------------------------------------
# DISPLAY SCORE
# ------------------------------------------

score_col1, score_col2 = st.columns([1, 2])

score_col1.metric(
    "🌍 Environmental Health Score",
    f"{environmental_health_score:.1f} / 100"
)


# ------------------------------------------
# DETERMINE ENVIRONMENTAL STATUS
# ------------------------------------------

if environmental_health_score >= 80:

    environmental_status = "🟢 Excellent Environmental Condition"

elif environmental_health_score >= 60:

    environmental_status = "🟡 Moderate Environmental Condition"

elif environmental_health_score >= 40:

    environmental_status = "🟠 Poor Environmental Condition"

else:

    environmental_status = "🔴 Critical Environmental Condition"


score_col2.markdown(
    f"""
    ### Current Environmental Status

    **{environmental_status}**

    This score is calculated using air quality, waste
    bin conditions, carbon emissions, environmental
    compliance, and pollution risk indicators.
    """
)
if page == "🏆 Zone Performance":
# ==========================================
# ZONE-WISE ENVIRONMENTAL PERFORMANCE RANKING
# ==========================================

     st.divider()

     st.markdown("## 🏆 Zone-Wise Environmental Performance Ranking")


# ------------------------------------------
# CALCULATE ZONE-WISE PERFORMANCE
# ------------------------------------------

zone_performance = (
    filtered_df
    .groupby("collection_zone")
    .agg(
        Average_AQI=("air_quality_index", "mean"),
        Average_Bin_Fill=("bin_fill_level_pct", "mean"),
        Average_Carbon_Emission=("carbon_emission_kg", "mean"),
        Compliance_Violations=(
            "compliance_status",
            lambda x: (x == "Violation").sum()
        ),
        Critical_Pollution_Alerts=(
            "pollution_risk_level",
            lambda x: (x == "Critical").sum()
        )
    )
    .reset_index()
)


# ------------------------------------------
# CALCULATE PERFORMANCE SCORE
# ------------------------------------------

zone_performance["AQI_Score"] = (
    100 - zone_performance["Average_AQI"] / 5
).clip(lower=0)

zone_performance["Bin_Score"] = (
    100 - zone_performance["Average_Bin_Fill"]
).clip(lower=0)

zone_performance["Carbon_Score"] = (
    100
    - (
        zone_performance["Average_Carbon_Emission"]
        / 120
    ) * 100
).clip(lower=0)


# Normalize violations and pollution alerts

max_violations = max(
    zone_performance["Compliance_Violations"].max(),
    1
)

max_critical_alerts = max(
    zone_performance[
        "Critical_Pollution_Alerts"
    ].max(),
    1
)


zone_performance["Compliance_Score"] = (
    100
    - (
        zone_performance["Compliance_Violations"]
        / max_violations
    ) * 100
)

zone_performance["Pollution_Score"] = (
    100
    - (
        zone_performance["Critical_Pollution_Alerts"]
        / max_critical_alerts
    ) * 100
)


# Final Environmental Performance Score

zone_performance["Environmental_Performance_Score"] = (
    zone_performance["AQI_Score"] * 0.30
    +
    zone_performance["Bin_Score"] * 0.20
    +
    zone_performance["Carbon_Score"] * 0.20
    +
    zone_performance["Compliance_Score"] * 0.15
    +
    zone_performance["Pollution_Score"] * 0.15
)


# ------------------------------------------
# CREATE RANKING
# ------------------------------------------

zone_performance = zone_performance.sort_values(
    by="Environmental_Performance_Score",
    ascending=False
)

zone_performance["Rank"] = range(
    1,
    len(zone_performance) + 1
)


# ------------------------------------------
# DISPLAY TOP AND LOWEST PERFORMING ZONES
# ------------------------------------------

best_zone = zone_performance.iloc[0]

worst_zone = zone_performance.iloc[-1]


best_col, worst_col = st.columns(2)

best_col.success(
    f"🥇 Best Performing Zone: "
    f"**{best_zone['collection_zone']}** "
    f"({best_zone['Environmental_Performance_Score']:.1f}/100)"
)

worst_col.error(
    f"⚠️ Highest Priority Zone: "
    f"**{worst_zone['collection_zone']}** "
    f"({worst_zone['Environmental_Performance_Score']:.1f}/100)"
)


# ------------------------------------------
# PERFORMANCE RANKING CHART
# ------------------------------------------

fig_ranking = px.bar(
    zone_performance,
    x="collection_zone",
    y="Environmental_Performance_Score",
    text="Rank",
    title="Environmental Performance Score by Zone",
    labels={
        "collection_zone": "Collection Zone",
        "Environmental_Performance_Score":
        "Performance Score (0-100)"
    }
)

fig_ranking.update_yaxes(
    range=[0, 100]
)

st.plotly_chart(
    fig_ranking,
    width="stretch"
)


# ------------------------------------------
# RANKING TABLE
# ------------------------------------------

st.markdown("### 📋 Detailed Zone Ranking")

ranking_display = zone_performance[
    [
        "Rank",
        "collection_zone",
        "Environmental_Performance_Score",
        "Average_AQI",
        "Average_Bin_Fill",
        "Average_Carbon_Emission",
        "Compliance_Violations",
        "Critical_Pollution_Alerts"
    ]
].copy()


# Round numerical values

ranking_display[
    "Environmental_Performance_Score"
] = ranking_display[
    "Environmental_Performance_Score"
].round(2)

ranking_display["Average_AQI"] = (
    ranking_display["Average_AQI"].round(2)
)

ranking_display["Average_Bin_Fill"] = (
    ranking_display["Average_Bin_Fill"].round(2)
)

ranking_display["Average_Carbon_Emission"] = (
    ranking_display[
        "Average_Carbon_Emission"
    ].round(2)
)


st.dataframe(
    ranking_display,
    width="stretch",
    hide_index=True
)
if page == "📋 Data Explorer":

    # ==========================================
    # FILTERED ENVIRONMENTAL DATA
    # ==========================================

    st.divider()

    st.markdown("## 📋 Environmental Data Explorer")

    # ------------------------------------------
    # DATA SUMMARY
    # ------------------------------------------

    data_col1, data_col2, data_col3 = st.columns(3)

    data_col1.metric(
        "📄 Total Records",
        len(filtered_df)
    )

    data_col2.metric(
        "🏙️ Zones Selected",
        filtered_df["collection_zone"].nunique()
    )

    data_col3.metric(
        "🏘️ Districts Selected",
        filtered_df["district"].nunique()
    )


    # ------------------------------------------
    # SEARCH RECORD
    # ------------------------------------------

    search_record = st.text_input(
        "🔍 Search by Record ID",
        placeholder="Example: SWM_100001"
    )

    if search_record:

        display_df = filtered_df[
            filtered_df["record_id"]
            .str.contains(
                search_record,
                case=False,
                na=False
            )
        ]

    else:

        display_df = filtered_df


    # ------------------------------------------
    # SELECT COLUMNS
    # ------------------------------------------

    available_columns = [
        "record_id",
        "collection_zone",
        "district",
        "waste_source",
        "waste_category",
        "waste_weight_kg",
        "bin_fill_level_pct",
        "air_quality_index",
        "carbon_emission_kg",
        "waste_risk_level",
        "pollution_risk_level",
        "compliance_status",
        "management_decision"
    ]

    selected_columns = st.multiselect(
        "📑 Select Columns to Display",
        options=available_columns,
        default=available_columns
    )


    # ------------------------------------------
    # DISPLAY DATA
    # ------------------------------------------

    st.markdown("### 📊 Filtered Dataset")

    if selected_columns:

        st.dataframe(
            display_df[selected_columns],
            width="stretch",
            hide_index=True
        )

    else:

        st.warning(
            "Please select at least one column."
        )


    # ------------------------------------------
    # DOWNLOAD FILTERED DATA
    # ------------------------------------------

    csv = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="ecowatch_filtered_data.csv",
        mime="text/csv"
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align: center;">
        <p>
            🌍 <b>EcoWatch AI</b> |
            Smart Waste, Pollution & Environmental Compliance Management
        </p>
        <p>
            Built for data-driven environmental monitoring and sustainable decision-making.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)    
