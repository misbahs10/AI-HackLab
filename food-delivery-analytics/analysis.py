"""
Food Delivery Analytics Challenge - Hackathon Task A
Author: Misbah Sajjad

Workflow: Load -> Clean -> Analyze -> Visualize -> Interpret -> Explain
"""

import pandas as pd #type: ignore
import matplotlib.pyplot as plt

# ============================================================
# STEP A: LOAD & UNDERSTAND
# ============================================================
print("=" * 60)
print("STEP A: LOAD & UNDERSTAND THE DATA")
print("=" * 60)

df = pd.read_csv("food_delivery_dataset.csv")

print(f"\nNumber of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

print("\nColumn names:")
print(list(df.columns))

print("\nData types:")
print(df.dtypes)

print("\nMissing values per column:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print(f"\nDuplicate rows: {df.duplicated().sum()}")

# ============================================================
# STEP B: CLEAN THE DATA
# ============================================================
print("\n" + "=" * 60)
print("STEP B: CLEAN THE DATA")
print("=" * 60)

rows_before = df.shape[0]

# 1. Fix Age: missing values -> filled with median age (robust to outliers)
df["Delivery_person_Age"] = df["Delivery_person_Age"].fillna(
    df["Delivery_person_Age"].median()
)
df["Delivery_person_Age"] = df["Delivery_person_Age"].astype(int)

# 2. Fix Ratings: missing values -> filled with median rating
df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].fillna(
    df["Delivery_person_Ratings"].median()
)

# 3. Fix Time_Orderd: missing values -> keep as "Unknown" (not used in our 3 questions,
#    so we don't drop rows just for this column)
df["Time_Orderd"] = df["Time_Orderd"].fillna("Unknown")

# 4. Convert Order_Date to proper datetime type
df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y", errors="coerce")

# 5. Clean text columns: strip extra spaces, standardize case
text_cols = ["Weather_conditions", "Road_traffic_density", "Type_of_order",
             "Type_of_vehicle", "Festival", "City", "delivery_speed"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# 6. Remove any duplicate rows (none found, but kept for safety/repeatability)
df = df.drop_duplicates()

# 7. Sanity check: remove impossible values (negative time/distance, if any)
df = df[(df["Time_taken (min)"] > 0) & (df["distance_km"] > 0)]

rows_after = df.shape[0]
print(f"\nRows before cleaning: {rows_before}")
print(f"Rows after cleaning:  {rows_after}")
print("\nMissing values after cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().sum() > 0 else "None")

# ============================================================
# STEP C: BASIC ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("STEP C: BASIC ANALYSIS")
print("=" * 60)

total_deliveries = len(df)
avg_time = df["Time_taken (min)"].mean()
min_time = df["Time_taken (min)"].min()
max_time = df["Time_taken (min)"].max()
avg_distance = df["distance_km"].mean()
avg_speed_kmph = (df["distance_km"] / (df["Time_taken (min)"] / 60)).mean()
avg_rating = df["Delivery_person_Ratings"].mean()
avg_age = df["Delivery_person_Age"].mean()

print(f"\nTotal deliveries: {total_deliveries}")
print(f"Average delivery time: {avg_time:.2f} min")
print(f"Minimum delivery time: {min_time} min")
print(f"Maximum delivery time: {max_time} min")
print(f"Average delivery distance: {avg_distance:.2f} km")
print(f"Average delivery speed: {avg_speed_kmph:.2f} km/h")
print(f"Average delivery-person rating: {avg_rating:.2f} / 5")
print(f"Average delivery-person age: {avg_age:.1f} years")

# ============================================================
# STEP D: ANSWER THE 3 COMPETITION QUESTIONS
# ============================================================
print("\n" + "=" * 60)
print("STEP D: COMPETITION QUESTIONS")
print("=" * 60)

# Q1: Which road traffic condition has the highest average delivery time?
traffic_avg_time = df.groupby("Road_traffic_density")["Time_taken (min)"].mean().sort_values(ascending=False)
q1_answer = traffic_avg_time.index[0]
print("\nQ1 - Traffic Impact:")
print(traffic_avg_time)
print(f"ANSWER: '{q1_answer}' traffic has the highest average delivery time "
      f"({traffic_avg_time.iloc[0]:.2f} min).")

# Q2: How does delivery distance affect delivery time?
correlation = df["distance_km"].corr(df["Time_taken (min)"])
print(f"\nQ2 - Distance Impact:")
print(f"Correlation between distance_km and Time_taken (min): {correlation:.3f}")
if correlation > 0.3:
    q2_answer = "Positive correlation: as distance increases, delivery time tends to increase."
elif correlation < -0.3:
    q2_answer = "Negative correlation: as distance increases, delivery time tends to decrease."
else:
    q2_answer = "Weak/no strong linear correlation between distance and delivery time."
print(f"ANSWER: {q2_answer}")

# Q3: Which combination of weather + traffic has the highest average delivery time?
combo_avg_time = (
    df.groupby(["Weather_conditions", "Road_traffic_density"])["Time_taken (min)"]
    .mean()
    .sort_values(ascending=False)
)
q3_weather, q3_traffic = combo_avg_time.index[0]
print(f"\nQ3 - Combined Conditions (top 5):")
print(combo_avg_time.head(5))
print(f"ANSWER: '{q3_weather}' weather + '{q3_traffic}' traffic has the highest "
      f"average delivery time ({combo_avg_time.iloc[0]:.2f} min).")

# ============================================================
# STEP D2: EXTRA ANALYSIS (beyond the 3 required questions,
# to demonstrate deeper Pandas skills)
# ============================================================
print("\n" + "=" * 60)
print("STEP D2: EXTRA ANALYSIS")
print("=" * 60)

# City-wise average delivery time
city_avg_time = df.groupby("City")["Time_taken (min)"].mean().sort_values(ascending=False)
print("\nAverage delivery time by City:")
print(city_avg_time)

# Vehicle type-wise average delivery time
vehicle_avg_time = df.groupby("Type_of_vehicle")["Time_taken (min)"].mean().sort_values(ascending=False)
print("\nAverage delivery time by Vehicle Type:")
print(vehicle_avg_time)

# Effect of Festival on delivery time
festival_avg_time = df.groupby("Festival")["Time_taken (min)"].mean()
print("\nAverage delivery time - Festival vs No Festival:")
print(festival_avg_time)

# Effect of multiple_deliveries on delivery time
multi_avg_time = df.groupby("multiple_deliveries")["Time_taken (min)"].mean().sort_index()
print("\nAverage delivery time by number of multiple deliveries:")
print(multi_avg_time)

# Effect of vehicle condition on delivery time
vehcond_avg_time = df.groupby("Vehicle_condition")["Time_taken (min)"].mean().sort_index()
print("\nAverage delivery time by Vehicle Condition (0=worst, 2=best):")
print(vehcond_avg_time)

# ============================================================
# STEP E: VISUALIZATIONS
# ============================================================
print("\n" + "=" * 60)
print("STEP E: CREATING VISUALIZATIONS")
print("=" * 60)

import os
os.makedirs("charts", exist_ok=True)

# Chart 1: Bar chart - Average delivery time by traffic density
plt.figure(figsize=(8, 5))
order = ["Low", "Medium", "High", "Jam"]
traffic_avg_time_ordered = traffic_avg_time.reindex(order)
bars = plt.bar(traffic_avg_time_ordered.index, traffic_avg_time_ordered.values,
                color=["#4CAF50", "#FFC107", "#FF9800", "#F44336"])
plt.title("Average Delivery Time by Traffic Density", fontsize=14, fontweight="bold")
plt.xlabel("Road Traffic Density")
plt.ylabel("Average Delivery Time (minutes)")
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f"{height:.1f}",
              ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("charts/chart1_traffic_vs_time.png", dpi=150)
plt.close()
print("Chart 1 saved: charts/chart1_traffic_vs_time.png")

# Chart 2: Scatter plot - Delivery distance vs delivery time
plt.figure(figsize=(8, 5))
sample = df.sample(n=min(3000, len(df)), random_state=42)  # sample for readable plot
plt.scatter(sample["distance_km"], sample["Time_taken (min)"],
            alpha=0.3, s=10, color="#2196F3")
plt.title("Delivery Distance vs Delivery Time", fontsize=14, fontweight="bold")
plt.xlabel("Distance (km)")
plt.ylabel("Time Taken (minutes)")
plt.tight_layout()
plt.savefig("charts/chart2_distance_vs_time.png", dpi=150)
plt.close()
print("Chart 2 saved: charts/chart2_distance_vs_time.png")

# Chart 3 (BONUS): Average delivery time by City and Festival - extra insight chart
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

city_avg_time.plot(kind="bar", ax=axes[0], color="#9C27B0")
axes[0].set_title("Avg Delivery Time by City", fontweight="bold")
axes[0].set_xlabel("City")
axes[0].set_ylabel("Avg Delivery Time (min)")
axes[0].tick_params(axis="x", rotation=20)

festival_avg_time.plot(kind="bar", ax=axes[1], color=["#607D8B", "#E91E63"])
axes[1].set_title("Avg Delivery Time: Festival vs Normal Days", fontweight="bold")
axes[1].set_xlabel("Festival")
axes[1].set_ylabel("Avg Delivery Time (min)")
axes[1].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig("charts/chart3_city_festival.png", dpi=150)
plt.close()
print("Chart 3 (bonus) saved: charts/chart3_city_festival.png")

# ============================================================
# STEP F: BUSINESS INSIGHTS
# ============================================================
print("\n" + "=" * 60)
print("STEP F: BUSINESS INSIGHTS")
print("=" * 60)

insights = [
    f"1. Traffic jams increase delivery time by ~{(traffic_avg_time['Jam'] - traffic_avg_time['Low']):.1f} minutes "
    f"compared to low-traffic conditions. The company should consider dynamic dispatch "
    f"(sending riders earlier or via alternate routes) during peak/jam hours.",

    f"2. Distance and delivery time are positively correlated ({correlation:.2f}), but the relationship "
    f"is moderate, not extremely strong -- meaning traffic and weather matter almost as much as raw "
    f"distance. Delivery-time estimates shown to customers should factor in live traffic, not just distance.",

    f"3. The worst-case combination is '{q3_weather}' weather with '{q3_traffic}' traffic "
    f"({combo_avg_time.iloc[0]:.1f} min average). The company could set customer expectations "
    f"(longer ETA warnings) or offer small delay-compensation during these specific conditions "
    f"to protect customer satisfaction.",

    f"4. Deliveries during festivals take almost DOUBLE the time ({festival_avg_time['Yes']:.1f} min) "
    f"compared to normal days ({festival_avg_time['No']:.1f} min). The company should plan for extra "
    f"riders and higher delivery-time buffers around festival dates.",

    f"5. Semi-Urban areas have by far the slowest deliveries ({city_avg_time['Semi-Urban']:.1f} min) "
    f"compared to Urban ({city_avg_time['Urban']:.1f} min) and Metropolitan ({city_avg_time['Metropolitian']:.1f} min) "
    f"areas -- likely due to fewer riders or longer road distances. The company should consider adding "
    f"more delivery partners in semi-urban zones.",
]

for insight in insights:
    print(f"\n{insight}")

# ============================================================
# STEP G: AI-POWERED EXPLANATION (Groq API)
# ============================================================
print("\n" + "=" * 60)
print("STEP G: AI-POWERED EXPLANATION")
print("=" * 60)

import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")

summary_for_ai = f"""
Total deliveries analyzed: {total_deliveries}
Average delivery time: {avg_time:.2f} minutes
Average delivery distance: {avg_distance:.2f} km
Average delivery speed: {avg_speed_kmph:.2f} km/h
Q1 - Traffic with highest avg delivery time: {q1_answer} ({traffic_avg_time.iloc[0]:.2f} min)
Q2 - Correlation between distance and delivery time: {correlation:.3f} ({q2_answer})
Q3 - Worst weather+traffic combination: {q3_weather} + {q3_traffic} ({combo_avg_time.iloc[0]:.2f} min)
"""

if not api_key:
    print("\n[INFO] GROQ_API_KEY not set. Skipping live AI call.")
    print("Set it with:  export GROQ_API_KEY='your_key_here'  (never hard-code it in the script)")
else:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a business analyst. Explain data findings "
                                           "in simple, clear language for a food-delivery company's management."},
            {"role": "user", "content": f"Here are the calculated results from our delivery data analysis:\n"
                                         f"{summary_for_ai}\n"
                                         f"Write a short (5-6 sentence) business explanation of what this means."}
        ],
    )
    ai_explanation = response.choices[0].message.content
    print("\nAI-Generated Business Explanation:\n")
    print(ai_explanation)

    with open("ai_explanation.txt", "w", encoding="utf-8") as f:
        f.write(ai_explanation)