import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# =========================
# SETTINGS
# =========================
NUM_RECORDS = 500000
OUTPUT_FILE = "cybernova_web_logs.csv"

np.random.seed(42)
random.seed(42)

# =========================
# OPTIONS
# =========================
countries = [
    "Botswana", "South Africa", "Namibia", "Zimbabwe", "Zambia",
    "Mozambique", "Kenya", "Nigeria", "Ghana", "Rwanda"
]

cities = {
    "Botswana": ["Gaborone", "Francistown", "Maun", "Palapye"],
    "South Africa": ["Johannesburg", "Cape Town", "Pretoria", "Durban"],
    "Namibia": ["Windhoek", "Swakopmund"],
    "Zimbabwe": ["Harare", "Bulawayo"],
    "Zambia": ["Lusaka", "Ndola"],
    "Mozambique": ["Maputo", "Beira"],
    "Kenya": ["Nairobi", "Mombasa"],
    "Nigeria": ["Lagos", "Abuja"],
    "Ghana": ["Accra", "Kumasi"],
    "Rwanda": ["Kigali"]
}

services = [
    "AI Cyber Assistant",
    "Real-Time Threat Monitoring",
    "Automated Risk Assessment",
    "Predictive System Maintenance",
    "Digital Infrastructure Prototyping"
]

request_types = [
    "Product Inquiry",
    "Schedule Demo",
    "Pricing Request",
    "AI Assistant Query",
    "Event Registration",
    "Technical Support"
]

traffic_sources = [
    "Direct",
    "Google Ads",
    "LinkedIn Ads",
    "Facebook",
    "Email Campaign",
    "Referral",
    "Organic Search"
]

campaign_names = [
    "CyberShield Launch",
    "SME Security Awareness",
    "Banking Cyber Resilience",
    "Government Digital Safety",
    "AI Assistant Webinar",
    "Threat Monitoring Promo"
]

campaign_types = [
    "Webinar",
    "Search Ads",
    "Social Media",
    "Email Campaign",
    "Referral Campaign",
    "Awareness Campaign"
]

customer_segments = [
    "SME",
    "Financial Institution",
    "Government Agency",
    "Large Enterprise",
    "Technology Partner"
]

subscription_types = [
    "Free Trial",
    "Basic",
    "Professional",
    "Enterprise"
]

device_types = ["Desktop", "Laptop", "Tablet", "Mobile"]
browsers = ["Chrome", "Edge", "Firefox", "Safari"]

response_codes = [200, 200, 200, 200, 200, 301, 400, 403, 404, 500]

# =========================
# GENERATE DATA
# =========================
start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 5, 15)
date_range_days = (end_date - start_date).days

records = []

for i in range(1, NUM_RECORDS + 1):
    country = random.choice(countries)
    city = random.choice(cities[country])
    service = random.choice(services)
    request_type = random.choice(request_types)
    traffic_source = random.choice(traffic_sources)
    customer_segment = random.choice(customer_segments)
    subscription_type = random.choice(subscription_types)

    timestamp = start_date + timedelta(
        days=random.randint(0, date_range_days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    engagement_score = np.random.randint(20, 101)
    time_on_page_seconds = np.random.randint(20, 900)
    pages_visited = np.random.randint(1, 15)

    bounce_rate = round(np.random.uniform(0.05, 0.85), 2)

    demo_requested = 1 if request_type == "Schedule Demo" or np.random.rand() < 0.12 else 0
    event_registered = 1 if request_type == "Event Registration" or np.random.rand() < 0.10 else 0
    ai_assistant_used = 1 if request_type == "AI Assistant Query" or np.random.rand() < 0.25 else 0

    # Sales probability based on engagement and behaviour
    sale_probability = 0.03
    sale_probability += 0.12 if demo_requested else 0
    sale_probability += 0.05 if ai_assistant_used else 0
    sale_probability += 0.04 if engagement_score > 70 else 0
    sale_probability += 0.03 if pages_visited > 6 else 0
    sale_probability -= 0.04 if bounce_rate > 0.65 else 0

    sale_confirmed = 1 if np.random.rand() < sale_probability else 0

    base_prices = {
        "AI Cyber Assistant": 6500,
        "Real-Time Threat Monitoring": 12000,
        "Automated Risk Assessment": 9000,
        "Predictive System Maintenance": 15000,
        "Digital Infrastructure Prototyping": 18000
    }

    revenue = base_prices[service] * sale_confirmed
    revenue += np.random.randint(500, 3000) if sale_confirmed else 0

    profit_margin = np.random.uniform(0.25, 0.55)
    profit = round(revenue * profit_margin, 2)

    customer_value = revenue + (engagement_score * 20) + (pages_visited * 50)

    service_rating = round(np.random.uniform(2.5, 5.0), 1) if sale_confirmed else round(np.random.uniform(1.5, 4.5), 1)

    renewal_status = random.choice(["Renewed", "Pending", "At Risk", "Not Applicable"])
    if subscription_type == "Free Trial":
        renewal_status = "Not Applicable"

    response_time_ms = int(np.random.normal(650, 250))
    response_time_ms = max(100, response_time_ms)

    response_code = random.choice(response_codes)
    error_flag = 1 if response_code != 200 or response_time_ms > 1200 else 0

    sales_target = base_prices[service] * np.random.uniform(0.8, 1.4)

    records.append({
        "log_id": i,
        "user_id": f"U{i:06d}",
        "session_id": f"S{np.random.randint(100000, 999999)}",
        "timestamp": timestamp,
        "date": timestamp.date(),
        "country": country,
        "city": city,
        "device_type": random.choice(device_types),
        "browser": random.choice(browsers),
        "service_name": service,
        "request_type": request_type,
        "traffic_source": traffic_source,
        "campaign_name": random.choice(campaign_names),
        "campaign_type": random.choice(campaign_types),
        "customer_segment": customer_segment,
        "subscription_type": subscription_type,
        "engagement_score": engagement_score,
        "time_on_page_seconds": time_on_page_seconds,
        "pages_visited": pages_visited,
        "bounce_rate": bounce_rate,
        "demo_requested": demo_requested,
        "event_registered": event_registered,
        "ai_assistant_used": ai_assistant_used,
        "sale_confirmed": sale_confirmed,
        "revenue": round(revenue, 2),
        "profit": profit,
        "customer_value": round(customer_value, 2),
        "service_rating": service_rating,
        "renewal_status": renewal_status,
        "response_time_ms": response_time_ms,
        "response_code": response_code,
        "error_flag": error_flag,
        "sales_target": round(sales_target, 2)
    })

# =========================
# SAVE DATA
# =========================
df = pd.DataFrame(records)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Dataset created successfully: {OUTPUT_FILE}")
print(f"Total records: {len(df):,}")
print(df.head())