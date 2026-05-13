import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="CyberNova Analytics Dashboard", layout="wide")

def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="dashboard-header">
        <h1>CyberNova Analytics Ltd</h1>
        <h2>Stakeholder-Driven Product Sales Analytics Dashboard</h2>
        <p>AI Cybersecurity | Digital Transformation | Business Intelligence | Sales & Marketing Analytics</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("cybernova_50k.csv", low_memory=False)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = pd.to_datetime(df["date"])

    category_columns = [
        "country", "city", "device_type", "browser", "service_name",
        "request_type", "traffic_source", "campaign_name", "campaign_type",
        "customer_segment", "subscription_type", "renewal_status"
    ]

    for col in category_columns:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df


df = load_data()


# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## CyberNova BI Platform")
st.sidebar.caption("Enterprise Analytics Dashboard")

role = st.sidebar.selectbox(
    "Select Stakeholder View",
    ["Management", "Sales Team", "Marketing Team", "IT Administrator"]
)

stakeholder_descriptions = {
    "Management": "Strategic growth, profitability, forecasting, and sustainability insights.",
    "Sales Team": "Lead prioritisation, conversions, and customer value analysis.",
    "Marketing Team": "Campaign performance, engagement, and market targeting insights.",
    "IT Administrator": "Operational monitoring, system reliability, and anomaly detection."
}

st.sidebar.markdown("---")
st.sidebar.subheader("Live Data Simulation")

live_mode = st.sidebar.checkbox("Enable Live Mode", value=False)

refresh_seconds = st.sidebar.selectbox(
    "Refresh Interval",
    [5, 10],
    index=0
)

live_sample_size = st.sidebar.selectbox(
    "Live Sample Size",
    [5000, 10000, 20000, 50000],
    index=1
)

if live_mode:
    refresh_count = st_autorefresh(
        interval=refresh_seconds * 1000,
        key="live_refresh"
    )

    df = df.sample(
        n=min(live_sample_size, len(df)),
        random_state=refresh_count
    ).sort_values("timestamp")

    st.success(
        f"Live Mode Active: dashboard refreshes every {refresh_seconds} seconds using {len(df):,} sampled records."
    )
else:
    refresh_count = 0
    st.info(f"Historical Mode Active: using dataset of {len(df):,} records.")

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("Upload CSV Data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, low_memory=False)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = pd.to_datetime(df["date"])
    st.sidebar.success("Uploaded dataset loaded successfully.")

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

min_date = df["date"].min()
max_date = df["date"].max()

date_range = st.sidebar.date_input(
    "Filter by Date Range",
    [min_date, max_date]
)

countries = st.sidebar.multiselect(
    "Filter by Country",
    sorted(df["country"].astype(str).unique()),
    default=sorted(df["country"].astype(str).unique())
)

services = st.sidebar.multiselect(
    "Filter by Service",
    sorted(df["service_name"].astype(str).unique()),
    default=sorted(df["service_name"].astype(str).unique())
)

customer_segments = st.sidebar.multiselect(
    "Filter by Customer Segment",
    sorted(df["customer_segment"].astype(str).unique()),
    default=sorted(df["customer_segment"].astype(str).unique())
)

traffic_sources = st.sidebar.multiselect(
    "Filter by Traffic Source",
    sorted(df["traffic_source"].astype(str).unique()),
    default=sorted(df["traffic_source"].astype(str).unique())
)

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
else:
    start_date = min_date
    end_date = max_date

filtered_df = df[
    (df["date"] >= start_date) &
    (df["date"] <= end_date) &
    (df["country"].astype(str).isin(countries)) &
    (df["service_name"].astype(str).isin(services)) &
    (df["customer_segment"].astype(str).isin(customer_segments)) &
    (df["traffic_source"].astype(str).isin(traffic_sources))
].copy()


# =========================
# PERFORMANCE PROTECTION
# =========================
MAX_ANALYSIS_ROWS = 100000

if len(filtered_df) > MAX_ANALYSIS_ROWS:
    filtered_df = filtered_df.sample(
        n=MAX_ANALYSIS_ROWS,
        random_state=42
    ).copy()

    # st.info(
#     f"Performance mode active: using a representative sample of {MAX_ANALYSIS_ROWS:,} records for dashboard analysis."
# )

# =========================
# SHARED CALCULATIONS
# =========================
total_requests = len(filtered_df)
total_revenue = filtered_df["revenue"].sum() if not filtered_df.empty else 0
total_profit = filtered_df["profit"].sum() if not filtered_df.empty else 0
confirmed_sales = filtered_df["sale_confirmed"].sum() if not filtered_df.empty else 0
demo_requests = filtered_df["demo_requested"].sum() if not filtered_df.empty else 0
event_registrations = filtered_df["event_registered"].sum() if not filtered_df.empty else 0
ai_interactions = filtered_df["ai_assistant_used"].sum() if not filtered_df.empty else 0
avg_engagement = filtered_df["engagement_score"].mean() if not filtered_df.empty else 0
avg_customer_value = filtered_df["customer_value"].mean() if not filtered_df.empty else 0
avg_service_rating = filtered_df["service_rating"].mean() if not filtered_df.empty else 0
avg_bounce_rate = filtered_df["bounce_rate"].mean() if not filtered_df.empty else 0
avg_response_time = filtered_df["response_time_ms"].mean() if not filtered_df.empty else 0
failed_requests = filtered_df["error_flag"].sum() if not filtered_df.empty else 0
error_rate = (failed_requests / total_requests) * 100 if total_requests > 0 else 0
conversion_rate = (confirmed_sales / total_requests) * 100 if total_requests > 0 else 0
total_target = filtered_df["sales_target"].sum() if not filtered_df.empty else 0
target_achieved_pct = (total_revenue / total_target) * 100 if total_target > 0 else 0

if not filtered_df.empty:
    filtered_df["lead_score"] = (
        filtered_df["engagement_score"] * 0.35
        + filtered_df["time_on_page_seconds"] * 0.015
        + filtered_df["pages_visited"] * 2
        + filtered_df["demo_requested"] * 20
        + filtered_df["ai_assistant_used"] * 10
        + filtered_df["event_registered"] * 10
        + filtered_df["customer_value"] * 0.002
        - filtered_df["bounce_rate"] * 15
    )

avg_lead_score = filtered_df["lead_score"].mean() if not filtered_df.empty else 0


# =========================
# HELPERS
# =========================
def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def insight(text):
    st.markdown(f"""
    <div class="insight-box">
    <b>Business Insight:</b><br>{text}
    </div>
    """, unsafe_allow_html=True)


def empty_check():
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return True
    return False


def live_note():
    if live_mode:
        st.caption(f"Live refresh cycle: {refresh_count} | Current visible records: {total_requests:,}")


# =========================
# MANAGEMENT DASHBOARD
# =========================
def management_executive_overview():
    section("Executive Overview")
    st.info("Management view focuses on strategic summaries, profitability, growth, and sustainability.")

    if empty_check():
        return

    live_note()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Revenue", f"BWP {total_revenue:,.0f}")
    c2.metric("Total Profit", f"BWP {total_profit:,.0f}")
    c3.metric("Conversion Rate", f"{conversion_rate:.2f}%")
    c4.metric("Avg Customer Value", f"BWP {avg_customer_value:,.0f}")
    c5.metric("Avg Rating", f"{avg_service_rating:.1f}/5")

    monthly = filtered_df.groupby(filtered_df["timestamp"].dt.to_period("M")).agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    ).reset_index()
    monthly["month"] = monthly["timestamp"].astype(str)

    fig = px.line(monthly, x="month", y=["revenue", "profit"], title="Revenue and Profit Trend")
    st.plotly_chart(fig, use_container_width=True, key="mgmt_revenue_profit_trend")

    col1, col2 = st.columns(2)

    with col1:
        segment_revenue = filtered_df.groupby("customer_segment", observed=True)["revenue"].sum().reset_index()
        fig = px.bar(segment_revenue, x="customer_segment", y="revenue", title="Revenue by Customer Segment")
        st.plotly_chart(fig, use_container_width=True, key="mgmt_revenue_segment")

    with col2:
        subscription_revenue = filtered_df.groupby("subscription_type", observed=True)["revenue"].sum().reset_index()
        fig = px.bar(subscription_revenue, x="subscription_type", y="revenue", title="Revenue by Subscription Type")
        st.plotly_chart(fig, use_container_width=True, key="mgmt_revenue_subscription")

    top_segment = segment_revenue.sort_values("revenue", ascending=False).iloc[0]["customer_segment"]
    top_subscription = subscription_revenue.sort_values("revenue", ascending=False).iloc[0]["subscription_type"]

    insight(
    f"""
    The strongest revenue contribution currently comes from the <b>{top_segment}</b> customer segment, while 
    <b>{top_subscription}</b> generates the highest subscription revenue. 
    This suggests that CyberNova’s profitability is concentrated within specific customer and subscription groups, 
    making these areas strategically important for long-term growth and sustainability.
    Management should prioritise retention strategies, premium service enhancements, and targeted expansion 
    campaigns focused on these high-performing customer groups.
    """
)


def management_strategic_growth():
    section("Strategic Growth")
    st.info("This view helps management identify which services, markets and customer groups support expansion and profitability.")

    if empty_check():
        return

    service_summary = filtered_df.groupby("service_name", observed=True).agg(
        demand=("log_id", "count"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        avg_rating=("service_rating", "mean"),
        sales=("sale_confirmed", "sum")
    ).reset_index()

    service_summary["conversion_rate"] = (service_summary["sales"] / service_summary["demand"] * 100).round(2)

    fig = px.scatter(
        service_summary,
        x="demand",
        y="revenue",
        size="profit",
        color="service_name",
        title="Strategic Service Opportunity: Demand vs Revenue",
        hover_data=["avg_rating", "conversion_rate"]
    )
    st.plotly_chart(fig, use_container_width=True, key="mgmt_service_opportunity")

    col1, col2 = st.columns(2)

    with col1:
        country_revenue = filtered_df.groupby("country", observed=True).agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            requests=("log_id", "count")
        ).reset_index()

        fig = px.choropleth(
            country_revenue,
            locations="country",
            locationmode="country names",
            color="revenue",
            title="Market Expansion: Revenue by Country"
        )
        st.plotly_chart(fig, use_container_width=True, key="mgmt_country_revenue_map")

    with col2:
        renewal = filtered_df["renewal_status"].value_counts().reset_index()
        renewal.columns = ["Renewal Status", "Count"]

        fig = px.pie(renewal, names="Renewal Status", values="Count", title="Renewal Status Distribution")
        st.plotly_chart(fig, use_container_width=True, key="mgmt_renewal_status")

    fig = px.bar(
        service_summary,
        x="service_name",
        y=["revenue", "profit"],
        barmode="group",
        title="Service Profitability Comparison"
    )
    st.plotly_chart(fig, use_container_width=True, key="mgmt_service_profitability")

    best_profit_service = service_summary.sort_values("profit", ascending=False).iloc[0]["service_name"]
    best_country = country_revenue.sort_values("revenue", ascending=False).iloc[0]["country"]

    insight(
    f"""
    <b>{best_profit_service}</b> currently delivers the strongest profitability performance, while 
    <b>{best_country}</b> demonstrates strong market potential through higher revenue contribution and engagement levels.
    This indicates an opportunity for CyberNova to strengthen competitive positioning within high-performing markets 
    and services.
    Management should consider increasing investment, targeted marketing, and strategic partnerships around these 
    high-value opportunities to support business expansion and revenue growth.
    """
)


def management_forecasting_risk():
    section("Forecasting & Risk")
    st.info("This section provides management with forward-looking insight and risk indicators.")

    if empty_check():
        return

    monthly = filtered_df.groupby(filtered_df["timestamp"].dt.to_period("M")).agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        demand=("log_id", "count")
    ).reset_index()

    monthly["month"] = monthly["timestamp"].astype(str)
    monthly["revenue_forecast"] = monthly["revenue"].rolling(3, min_periods=1).mean()
    monthly["profit_forecast"] = monthly["profit"].rolling(3, min_periods=1).mean()

    fig = px.line(
        monthly,
        x="month",
        y=["revenue", "revenue_forecast", "profit", "profit_forecast"],
        title="Revenue and Profit Moving Average Forecast"
    )
    st.plotly_chart(fig, use_container_width=True, key="mgmt_forecast")

    daily = filtered_df.groupby("date").agg(requests=("log_id", "count")).reset_index()
    mean_requests = daily["requests"].mean()
    std_requests = daily["requests"].std()
    daily["z_score"] = (daily["requests"] - mean_requests) / std_requests if std_requests > 0 else 0
    daily["anomaly"] = daily["z_score"].abs() > 2

    fig = px.scatter(
        daily,
        x="date",
        y="requests",
        color="anomaly",
        title="Business Risk Indicator: Unusual Demand Spikes",
        hover_data=["z_score"]
    )
    if len(monthly) >= 2 and monthly.iloc[-1]["revenue"] > monthly.iloc[0]["revenue"]:
        insight(
        """
        Revenue trends indicate positive business growth over time, supported by increasing customer demand and 
        service engagement.
        This suggests that current business strategies and service offerings are generating sustainable commercial value.
        Management should continue scaling high-performing services while proactively preparing infrastructure, 
        staffing, and operational resources to support future growth.
        """
        )
    else:
        insight(
        """
        Revenue trends indicate inconsistent or slowing growth patterns, which may affect long-term profitability 
        and competitiveness.
        This may suggest declining customer engagement, weaker market performance, or reduced service demand.
        Management should review pricing strategies, campaign performance, customer retention efforts, and service 
        competitiveness to improve growth performance.
        """
        )

# =========================
# SALES DASHBOARD
# =========================
def sales_overview():
    section("Sales Overview")
    st.info("Sales view focuses on conversions, demo requests, lead quality and service-level sales performance.")

    if empty_check():
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Demo Requests", f"{demo_requests:,}")
    c2.metric("Confirmed Sales", f"{confirmed_sales:,}")
    c3.metric("Conversion Rate", f"{conversion_rate:.2f}%")
    c4.metric("Target Achieved", f"{target_achieved_pct:.2f}%")
    c5.metric("Avg Lead Score", f"{avg_lead_score:.1f}")

    funnel_data = pd.DataFrame({
        "Stage": ["Total Requests", "Demo Requests", "Confirmed Sales"],
        "Count": [total_requests, demo_requests, confirmed_sales]
    })

    fig = px.funnel(funnel_data, x="Count", y="Stage", title="Sales Funnel: Interest to Confirmed Sale")
    st.plotly_chart(fig, use_container_width=True, key="sales_funnel")

    service_sales = filtered_df.groupby("service_name", observed=True).agg(
        requests=("log_id", "count"),
        demos=("demo_requested", "sum"),
        sales=("sale_confirmed", "sum"),
        revenue=("revenue", "sum"),
        customer_value=("customer_value", "mean")
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(service_sales, x="service_name", y="sales", title="Confirmed Sales by Service")
        st.plotly_chart(fig, use_container_width=True, key="sales_confirmed_service")

    with col2:
        fig = px.scatter(
            service_sales,
            x="demos",
            y="sales",
            size="customer_value",
            color="service_name",
            title="Demo Requests vs Confirmed Sales"
        )
        st.plotly_chart(fig, use_container_width=True, key="sales_demo_vs_sales")

    best_service = service_sales.sort_values("sales", ascending=False).iloc[0]["service_name"]
    insight(
    f"""
    <b>{best_service}</b> currently generates the highest confirmed sales performance, indicating strong customer demand 
    and conversion effectiveness.
    This suggests that the service aligns well with customer needs and represents one of CyberNova’s strongest revenue opportunities.
    The sales team should prioritise upselling, targeted demonstrations, and follow-up engagement around this service 
    to maximise conversions and revenue growth.
    """
)

def sales_lead_prioritisation():
    section("Lead Prioritisation")
    st.info("This section helps sales identify customers most likely to convert or generate high value.")

    if empty_check():
        return

    sales_df = filtered_df.copy()

    sales_df["lead_priority"] = pd.cut(
        sales_df["lead_score"],
        bins=[-100, 40, 70, 300],
        labels=["Low Priority", "Medium Priority", "High Priority"],
        include_lowest=True
    )

    priority_summary = sales_df["lead_priority"].value_counts().reset_index()
    priority_summary.columns = ["Lead Priority", "Count"]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(priority_summary, names="Lead Priority", values="Count", title="Lead Priority Distribution")
        st.plotly_chart(fig, use_container_width=True, key="sales_lead_priority")

    with col2:
        segment_value = sales_df.groupby("customer_segment", observed=True).agg(
            avg_lead_score=("lead_score", "mean"),
            avg_customer_value=("customer_value", "mean")
        ).reset_index()

        fig = px.bar(
            segment_value,
            x="customer_segment",
            y=["avg_lead_score", "avg_customer_value"],
            barmode="group",
            title="Lead Quality by Customer Segment"
        )
        st.plotly_chart(fig, use_container_width=True, key="sales_segment_quality")

    fig = px.scatter(
        sales_df,
        x="engagement_score",
        y="customer_value",
        color="sale_confirmed",
        size="pages_visited",
        title="Engagement vs Customer Value",
        hover_data=["service_name", "customer_segment", "lead_score"]
    )
    st.plotly_chart(fig, use_container_width=True, key="sales_engagement_value")

    st.subheader("Top 20 High-Value Leads")
    top_leads = sales_df.sort_values("lead_score", ascending=False).head(20)
    st.dataframe(
        top_leads[
            [
                "log_id",
                "user_id",
                "country",
                "customer_segment",
                "service_name",
                "request_type",
                "traffic_source",
                "engagement_score",
                "pages_visited",
                "customer_value",
                "lead_score",
                "lead_priority"
            ]
        ],
        use_container_width=True
    )

    high_priority_count = (sales_df["lead_priority"] == "High Priority").sum()
    insight(
    f"""
    The system identified <b>{high_priority_count:,}</b> high-priority leads with strong engagement behaviour, 
    higher customer value, and increased likelihood of conversion.
    This enables the sales team to focus effort on the most commercially valuable prospects instead of distributing 
    resources evenly across all customers.
    Prioritising these leads may improve conversion efficiency, increase sales productivity, and maximise return on sales effort.
    """
)

def sales_service_conversion():
    section("Service Conversion")
    st.info("This section helps sales understand which services convert best and where follow-up should improve.")

    if empty_check():
        return

    conversion = filtered_df.groupby("service_name", observed=True).agg(
        requests=("log_id", "count"),
        demos=("demo_requested", "sum"),
        sales=("sale_confirmed", "sum"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    ).reset_index()

    conversion["conversion_rate"] = (conversion["sales"] / conversion["requests"] * 100).round(2)

    fig = px.bar(conversion, x="service_name", y="conversion_rate", title="Conversion Rate by Service")
    st.plotly_chart(fig, use_container_width=True, key="sales_conversion_rate")

    fig = px.bar(
        conversion,
        x="service_name",
        y=["revenue", "profit"],
        barmode="group",
        title="Revenue and Profit by Service"
    )
    st.plotly_chart(fig, use_container_width=True, key="sales_revenue_profit")

    best_conversion = conversion.sort_values("conversion_rate", ascending=False).iloc[0]["service_name"]
    insight(
    f"""
    <b>{best_conversion}</b> currently demonstrates the strongest conversion performance across available services.
    This indicates that customer interest in this service is more effectively translated into confirmed sales, 
    making it a high-performing commercial offering.
    Sales and marketing teams should investigate the factors contributing to this success and apply similar strategies 
    to lower-performing services.
    """
)

# =========================
# MARKETING DASHBOARD
# =========================
def marketing_overview():
    section("Marketing Overview")
    st.info("Marketing view focuses on traffic quality, campaign performance, engagement and market targeting.")

    if empty_check():
        return

    traffic_sales = filtered_df.groupby("traffic_source", observed=True).agg(
        visits=("log_id", "count"),
        sales=("sale_confirmed", "sum"),
        engagement=("engagement_score", "mean"),
        bounce_rate=("bounce_rate", "mean")
    ).reset_index()

    traffic_sales["traffic_to_sale"] = (traffic_sales["sales"] / traffic_sales["visits"] * 100).round(2)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Website Visits", f"{total_requests:,}")
    c2.metric("Avg Engagement", f"{avg_engagement:.1f}")
    c3.metric("Event Registrations", f"{event_registrations:,}")
    c4.metric("AI Interactions", f"{ai_interactions:,}")
    c5.metric("Avg Bounce Rate", f"{avg_bounce_rate:.2f}")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(traffic_sales, x="traffic_source", y="visits", title="Website Visits by Traffic Source")
        st.plotly_chart(fig, use_container_width=True, key="marketing_visits_source")

    with col2:
        fig = px.bar(
            traffic_sales,
            x="traffic_source",
            y="traffic_to_sale",
            title="Traffic-to-Sale Conversion by Source"
        )
        st.plotly_chart(fig, use_container_width=True, key="marketing_source_conversion")

    campaign = filtered_df.groupby(["campaign_name", "campaign_type"], observed=True).agg(
        visits=("log_id", "count"),
        demos=("demo_requested", "sum"),
        events=("event_registered", "sum"),
        ai_interactions=("ai_assistant_used", "sum"),
        avg_engagement=("engagement_score", "mean")
    ).reset_index()

    fig = px.bar(
        campaign,
        x="campaign_name",
        y=["demos", "events", "ai_interactions"],
        barmode="group",
        title="Campaign Engagement Performance",
        hover_data=["campaign_type", "avg_engagement"]
    )
    st.plotly_chart(fig, use_container_width=True, key="marketing_campaign_engagement")

    best_campaign = campaign.sort_values("avg_engagement", ascending=False).iloc[0]["campaign_name"]
    insight(
    f"""
    <b>{best_campaign}</b> currently generates the highest customer engagement levels across active campaigns.
    Strong engagement suggests that the campaign messaging, targeting strategy, or promotional approach is effectively 
    attracting customer attention and interaction.
    Marketing teams should consider increasing investment in similar campaign strategies while analysing what elements 
    contributed to the campaign’s success.
    """
)

def marketing_customer_behaviour():
    section("Customer Behaviour")
    st.info("This section helps marketing understand what visitors are interested in and how they behave online.")

    if empty_check():
        return

    col1, col2 = st.columns(2)

    with col1:
        request_type = filtered_df["request_type"].value_counts().reset_index()
        request_type.columns = ["Request Type", "Count"]
        fig = px.pie(request_type, names="Request Type", values="Count", title="Request Type Distribution")
        st.plotly_chart(fig, use_container_width=True, key="marketing_request_type")

    with col2:
        device = filtered_df["device_type"].value_counts().reset_index()
        device.columns = ["Device Type", "Count"]
        fig = px.pie(device, names="Device Type", values="Count", title="Device Type Distribution")
        st.plotly_chart(fig, use_container_width=True, key="marketing_device_type")

    behaviour = filtered_df.groupby("service_name", observed=True).agg(
        visits=("log_id", "count"),
        avg_pages=("pages_visited", "mean"),
        avg_time=("time_on_page_seconds", "mean"),
        avg_bounce=("bounce_rate", "mean"),
        ai_interactions=("ai_assistant_used", "sum")
    ).reset_index()

    fig = px.bar(
        behaviour,
        x="service_name",
        y=["avg_pages", "avg_time", "ai_interactions"],
        barmode="group",
        title="Customer Behaviour by Service"
    )
    st.plotly_chart(fig, use_container_width=True, key="marketing_behaviour_service")

    fig = px.scatter(
        behaviour,
        x="avg_bounce",
        y="avg_time",
        size="visits",
        color="service_name",
        title="Bounce Rate vs Time on Page"
    )
    st.plotly_chart(fig, use_container_width=True, key="marketing_bounce_time")

    top_interest = behaviour.sort_values("visits", ascending=False).iloc[0]["service_name"]
    insight(
    f"""
    Customer activity indicates that <b>{top_interest}</b> currently attracts the highest level of visitor interest and interaction.
    Higher engagement around this service suggests strong market demand and customer relevance.
    Marketing teams should strengthen promotional activities, content strategies, and customer engagement initiatives 
    related to this service to maximise conversions and market visibility.
    """
)

def marketing_market_targeting():
    section("Market Targeting")
    st.info("This section supports campaign targeting by showing which regions and segments are most engaged.")

    if empty_check():
        return

    country = filtered_df.groupby("country", observed=True).agg(
        visits=("log_id", "count"),
        avg_engagement=("engagement_score", "mean"),
        sales=("sale_confirmed", "sum"),
        revenue=("revenue", "sum")
    ).reset_index()

    fig = px.bar(country, x="country", y="visits", title="Website Visits by Country")
    st.plotly_chart(fig, use_container_width=True, key="marketing_country_visits")

    fig = px.scatter(
        country,
        x="visits",
        y="avg_engagement",
        size="revenue",
        color="country",
        title="Market Targeting: Visits vs Engagement by Country",
        hover_data=["sales"]
    )
    st.plotly_chart(fig, use_container_width=True, key="marketing_country_engagement")

    segment_interest = filtered_df.groupby(["customer_segment", "service_name"], observed=True).agg(
        requests=("log_id", "count")
    ).reset_index()

    fig = px.bar(
        segment_interest,
        x="customer_segment",
        y="requests",
        color="service_name",
        title="Service Interest by Customer Segment"
    )
    st.plotly_chart(fig, use_container_width=True, key="marketing_segment_interest")

    best_country = country.sort_values("avg_engagement", ascending=False).iloc[0]["country"]
    insight(
    f"""
    <b>{best_country}</b> currently demonstrates the strongest customer engagement levels among analysed markets.
    This suggests higher market responsiveness and stronger potential for campaign effectiveness and customer acquisition.
    Marketing teams should prioritise targeted campaigns, regional promotions, and market expansion strategies within 
    this region to maximise growth opportunities.
    """
)

# =========================
# IT DASHBOARD
# =========================
def it_system_health():
    section("System Health")
    st.info("IT view focuses on system reliability, response times, errors and data monitoring.")

    if empty_check():
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Avg Response Time", f"{avg_response_time:.0f} ms")
    c2.metric("Error Rate", f"{error_rate:.2f}%")
    c3.metric("Total Requests", f"{total_requests:,}")
    c4.metric("Error Flags", f"{failed_requests:,}")
    c5.metric("Live Mode", "ON" if live_mode else "OFF")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(filtered_df, x="response_time_ms", nbins=50, title="Response Time Distribution")
        st.plotly_chart(fig, use_container_width=True, key="it_response_time")

    with col2:
        response_codes = filtered_df["response_code"].value_counts().reset_index()
        response_codes.columns = ["Response Code", "Count"]
        fig = px.bar(response_codes, x="Response Code", y="Count", title="HTTP Response Code Distribution")
        st.plotly_chart(fig, use_container_width=True, key="it_response_codes")

    daily = filtered_df.groupby("date").agg(
        requests=("log_id", "count"),
        avg_response_time=("response_time_ms", "mean"),
        errors=("error_flag", "sum")
    ).reset_index()

    fig = px.line(
        daily,
        x="date",
        y=["requests", "avg_response_time", "errors"],
        title="Requests, Response Time and Errors Over Time"
    )
    st.plotly_chart(fig, use_container_width=True, key="it_health_trend")

    if avg_response_time > 1000:
        insight(
            """
            System response times are currently elevated, which may negatively affect user experience, customer satisfaction, 
            and conversion performance.
            Slow performance may also indicate infrastructure strain or inefficient resource allocation during higher demand periods.
            IT administrators should investigate server optimisation, infrastructure scaling, and performance monitoring 
            strategies to maintain system reliability.
            """
        )
    else:
        insight(
            """
            System response times remain within an acceptable operational range, indicating stable platform performance 
            and satisfactory user experience.
            Stable performance supports customer engagement, operational reliability, and business continuity.
            IT administrators should continue monitoring traffic behaviour and infrastructure performance to maintain service quality.
            """
        )

def it_data_validation():
    section("Data Validation")
    st.info("This section verifies whether uploaded or generated datasets are suitable for analysis.")

    if empty_check():
        return

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download Current Filtered Data as CSV",
        data=csv,
        file_name="filtered_cybernova_data.csv",
        mime="text/csv"
    )

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head(100), use_container_width=True)

    st.subheader("Missing Values")
    missing_values = filtered_df.isnull().sum().reset_index()
    missing_values.columns = ["Column", "Missing Values"]
    st.dataframe(missing_values, use_container_width=True)

    st.subheader("Descriptive Statistics")
    st.dataframe(filtered_df.describe(), use_container_width=True)

    insight(
    """
    Data validation processes help ensure that analytical outputs remain accurate, reliable, and suitable for business decision-making.
    Reviewing missing values, dataset structure, and descriptive statistics reduces the risk of misleading insights 
    and improves overall analytical confidence.
    IT administrators and analysts should regularly monitor data quality to maintain the reliability of dashboard reporting and forecasting.
    """
)

def it_operational_monitoring():
    section("Operational Monitoring")
    st.info("This section helps IT detect unusual activity patterns and operational risks.")

    if empty_check():
        return

    daily = filtered_df.groupby("date").agg(
        requests=("log_id", "count"),
        avg_response_time=("response_time_ms", "mean"),
        errors=("error_flag", "sum")
    ).reset_index()

    mean_requests = daily["requests"].mean()
    std_requests = daily["requests"].std()

    daily["z_score"] = (daily["requests"] - mean_requests) / std_requests if std_requests > 0 else 0
    daily["anomaly"] = daily["z_score"].abs() > 2

    fig = px.scatter(
        daily,
        x="date",
        y="requests",
        color="anomaly",
        size="errors",
        title="Traffic Spike and Anomaly Detection",
        hover_data=["z_score", "avg_response_time", "errors"]
    )
    st.plotly_chart(fig, use_container_width=True, key="it_anomaly_detection")

    fig = px.line(
        daily,
        x="date",
        y=["avg_response_time", "errors"],
        title="Operational Risk Trend: Response Time and Errors"
    )
    st.plotly_chart(fig, use_container_width=True, key="it_operational_risk")

    anomaly_count = daily["anomaly"].sum()

    if anomaly_count > 0:
        insight(f"<b>{anomaly_count}</b> unusual traffic day(s) detected. IT should review these periods.")
    else:
        insight("No major unusual traffic patterns detected in the selected data.")
    
    if anomaly_count > 0:
        insight(
            f"""
            The system detected <b>{anomaly_count}</b> unusual traffic period(s), indicating abnormal operational activity patterns.
            These anomalies may reflect sudden customer demand spikes, operational instability, infrastructure stress, or 
            potential cybersecurity concerns.
            IT administrators should investigate these periods further to determine root causes and minimise operational risk.
            """
        )
    else:
        insight(
            """
            No significant abnormal traffic behaviour was detected within the selected analysis period.
            This suggests stable operational activity and consistent system performance across the monitored environment.
            Continued monitoring remains important to detect future operational risks or unexpected activity changes early.
            """
        )

# =========================
# ROLE-BASED RENDERING
# =========================
if role == "Management":
    tabs = st.tabs(["Executive Overview", "Strategic Growth", "Forecasting & Risk"])

    with tabs[0]:
        management_executive_overview()
    with tabs[1]:
        management_strategic_growth()
    with tabs[2]:
        management_forecasting_risk()

elif role == "Sales Team":
    tabs = st.tabs(["Sales Overview", "Lead Prioritisation", "Service Conversion"])

    with tabs[0]:
        sales_overview()
    with tabs[1]:
        sales_lead_prioritisation()
    with tabs[2]:
        sales_service_conversion()

elif role == "Marketing Team":
    tabs = st.tabs(["Marketing Overview", "Customer Behaviour", "Market Targeting"])

    with tabs[0]:
        marketing_overview()
    with tabs[1]:
        marketing_customer_behaviour()
    with tabs[2]:
        marketing_market_targeting()

else:
    tabs = st.tabs(["System Health", "Data Validation", "Operational Monitoring"])

    with tabs[0]:
        it_system_health()
    with tabs[1]:
        it_data_validation()
    with tabs[2]:
        it_operational_monitoring()