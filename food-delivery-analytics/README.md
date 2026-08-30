# Food Delivery Analytics Challenge — Hackathon Task A

## Objective
Analyze a food-delivery dataset using Python and Pandas (no Machine Learning) to
find insights that help a food-delivery company improve delivery performance.

## Dataset
`food_delivery_dataset.csv` — 38,964 delivery records, 22 columns (delivery-person
info, location, order timing, weather, traffic, vehicle condition, distance,
delivery time, etc.)

## How to Run
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. (Optional, for Step G) Set your Groq API key as an environment variable —
   never hard-code it in the script:
   ```
   export GROQ_API_KEY="your_key_here"
   ```
3. Run the analysis:
   ```
   python analysis.py
   ```
4. Charts are saved to the `charts/` folder.

## Data Cleaning Decisions
- **Delivery_person_Age** (1,019 missing) → filled with the median age. Median
  is used instead of mean because it is not skewed by outliers.
- **Delivery_person_Ratings** (1,055 missing) → filled with the median rating,
  for the same reason.
- **Time_Orderd** (835 missing) → filled with `"Unknown"` instead of dropping
  rows, since this column is not required for the 3 competition questions and
  dropping rows would lose otherwise-valid data.
- **Order_Date** → converted from text to a proper `datetime` type.
- **Text columns** (Weather_conditions, Road_traffic_density, Type_of_order,
  Type_of_vehicle, Festival, City, delivery_speed) → stripped of extra
  whitespace for consistency.
- **Duplicates** → checked and removed (none were found in this dataset).
- **Invalid rows** → any row with non-positive delivery time or distance would
  be removed (none were found).

## Basic Statistics
- Total deliveries: 38,964
- Average delivery time: 26.58 minutes
- Average delivery distance: 9.77 km
- Average delivery speed: ~23.6 km/h
- Average delivery-person rating: 4.63 / 5
- Average delivery-person age: 29.6 years

## Answers to the 3 Competition Questions

**Q1 — Traffic Impact:** "Jam" traffic conditions have the highest average
delivery time (31.44 min), followed by High (27.41), Medium (26.93), and Low
(21.50 min).

**Q2 — Distance Impact:** There is a positive correlation (0.322) between
distance and delivery time — deliveries covering more distance generally take
longer, though the relationship is moderate (traffic and weather also play a
large role).

**Q3 — Combined Conditions:** The combination of **Fog weather + Jam traffic**
has the highest average delivery time (36.89 minutes), followed closely by
Cloudy + Jam (36.71 min).

## Business Insights
1. Traffic jams add roughly **10 extra minutes** per delivery compared to
   low-traffic conditions — the company should consider smarter dispatch
   timing or route changes during jam hours.
2. Distance alone doesn't fully explain delivery time (correlation is only
   moderate) — live traffic and weather should be factored into the ETA shown
   to customers, not distance alone.
3. Fog + Jam is the worst-case scenario for delivery time — setting realistic
   customer expectations (or small compensation) during these specific
   conditions can help protect customer satisfaction.
4. **Festival deliveries take almost double the time** (45.5 min vs. 26.2 min
   on normal days) — the company should schedule extra riders and set higher
   delivery-time buffers around festival dates.
5. **Semi-Urban areas are by far the slowest** (49.7 min average) compared to
   Urban (23.2 min) and Metropolitan (27.4 min) areas — likely due to fewer
   available riders or longer road distances, suggesting the company should
   add more delivery partners in semi-urban zones.

## Extra Analysis (beyond the 3 required questions)
To demonstrate deeper Pandas skills, the script also analyzes:
- Average delivery time by City
- Average delivery time by Vehicle Type
- Effect of Festival days on delivery time
- Effect of number of multiple deliveries on delivery time
- Effect of vehicle condition on delivery time

## Visualizations
- `charts/chart1_traffic_vs_time.png` — Bar chart of average delivery time by
  traffic density.
- `charts/chart2_distance_vs_time.png` — Scatter plot of delivery distance vs.
  delivery time.
- `charts/chart3_city_festival.png` — (Bonus) Side-by-side comparison of
  delivery time by City and by Festival vs. Normal days.

## AI-Powered Explanation
Step G uses the **Groq API** (`llama-3.1-8b-instant`) to turn the calculated
Pandas results into a short, plain-language business explanation. The API key
is read from the `GROQ_API_KEY` environment variable and is never hard-coded.

## Notes
- No Machine Learning model is trained anywhere in this project, per the task
  requirements — all analysis is done with Pandas.
- All 3 competition questions are answered programmatically (via `groupby`
  and `.corr()`), not hard-coded.

## Bonus: Streamlit Dashboard
An interactive dashboard (`app.py`) is included as a bonus feature. It lets you
filter the data by City, Weather, Traffic, Vehicle Type, and Festival, and
shows live-updating KPIs, charts, the 3 competition question answers, business
insights, and an AI explanation button (Groq).

Run it with:
```
streamlit run app.py
```
Then open the local URL it prints (usually http://localhost:8501) in your
browser. Enter your Groq API key directly in the dashboard's password field
to generate the AI explanation (it is not stored anywhere).