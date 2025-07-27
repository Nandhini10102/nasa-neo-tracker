import streamlit as st
import mysql.connector
import pandas as pd

# 📌 DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Riya#2021",
    database="nasa_neo1"
)
cursor = conn.cursor()

st.set_page_config(page_title="NASA Asteroid Tracker", layout="wide")
st.markdown("<h1 style='text-align: center;'>🚀 NASA Asteroid Tracker</h1>", unsafe_allow_html=True)

# Sidebar Main Navigation
menu = st.sidebar.radio("📂 Select Section", ["🪐 Asteroid", "📅 Approaches", "📊 Queries"])

# Base SQL
base_query = """
SELECT 
    a.name, ca.close_approach_date, ca.relative_velocity_kmph, 
    ca.miss_distance_lunar, ca.astronomical, 
    a.estimated_diameter_min_km, a.estimated_diameter_max_km, 
    a.is_potentially_hazardous_asteroid, ca.orbiting_body
FROM close_approach ca
JOIN asteroids a ON ca.neo_reference_id = a.id
"""

if menu == "🪐 Asteroid":
    st.sidebar.header("🛠️ Filter Criteria")

    query_options = [
        "All Close Approaches",
        "Potentially Hazardous Only",
        "Velocity > 50,000 km/h",
        "Came Within 1 Lunar Distance",
        "Came Within 0.05 AU",
        "Custom Filtered View"
    ]
    selected_query = st.sidebar.selectbox("📄 Select a query", query_options)

    selected_date = st.sidebar.date_input("📅 Close Approach Date (optional)")
    velocity = st.sidebar.slider("💨 Min Relative Velocity (km/h)", 0, 150000, 0)
    astronomical = st.sidebar.slider("🌍 Max Astronomical Distance (AU)", 0.0, 1.0, 1.0)
    lunar = st.sidebar.slider("🌕 Max Lunar Distance", 0.0, 100.0, 100.0)
    diameter = st.sidebar.slider("📏 Min Estimated Diameter (km)", 0.0, 10.0, 0.0)
    hazard = st.sidebar.selectbox("☢️ Hazardous", ["All", "True", "False"])

    # Build SQL based on query selected
    if selected_query == "All Close Approaches":
        final_query = base_query + " LIMIT 1000"

    elif selected_query == "Potentially Hazardous Only":
        final_query = base_query + " WHERE a.is_potentially_hazardous_asteroid = TRUE LIMIT 1000"

    elif selected_query == "Velocity > 50,000 km/h":
        final_query = base_query + " WHERE ca.relative_velocity_kmph > 50000 LIMIT 1000"

    elif selected_query == "Came Within 1 Lunar Distance":
        final_query = base_query + " WHERE ca.miss_distance_lunar < 1 LIMIT 1000"

    elif selected_query == "Came Within 0.05 AU":
        final_query = base_query + " WHERE ca.astronomical < 0.05 LIMIT 1000"

    elif selected_query == "Custom Filtered View":
        filters = []
        if selected_date:
            filters.append(f"ca.close_approach_date = '{selected_date}'")
        if velocity:
            filters.append(f"ca.relative_velocity_kmph >= {velocity}")
        if astronomical:
            filters.append(f"ca.astronomical <= {astronomical}")
        if lunar:
            filters.append(f"ca.miss_distance_lunar <= {lunar}")
        if diameter > 0:
            filters.append(f"a.estimated_diameter_min_km >= {diameter}")
        if hazard == "True":
            filters.append("a.is_potentially_hazardous_asteroid = TRUE")
        elif hazard == "False":
            filters.append("a.is_potentially_hazardous_asteroid = FALSE")

        final_query = base_query
        if filters:
            final_query += " WHERE " + " AND ".join(filters)
        final_query += " LIMIT 1000"

    # Run and show result
    cursor.execute(final_query)
    result = cursor.fetchall()
    cols = [col[0] for col in cursor.description]
    df = pd.DataFrame(result, columns=cols)

    st.subheader("📌 Filtered Asteroids")
    st.dataframe(df, use_container_width=True)

elif menu == "📅 Approaches":
    st.subheader("📅 All Approaches (Latest 1000)")

    query = base_query + " ORDER BY ca.close_approach_date DESC LIMIT 1000"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

    st.dataframe(df, use_container_width=True)

elif menu == "📊 Queries":
    st.subheader("📊 Run Predefined SQL Queries")

    query_map = {
        "1️⃣ All hazardous asteroids": """
            SELECT * FROM asteroids WHERE is_potentially_hazardous_asteroid = TRUE
        """,
        "2️⃣ Asteroids within 1 lunar distance": """
            SELECT a.name, ca.miss_distance_lunar FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            WHERE ca.miss_distance_lunar < 1
        """,
        "3️⃣ Top 5 fastest asteroids": """
            SELECT a.name, ca.relative_velocity_kmph FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            ORDER BY ca.relative_velocity_kmph DESC LIMIT 5
        """,
        "4️⃣ Largest estimated diameter": """
            SELECT name, estimated_diameter_max_km FROM asteroids
            ORDER BY estimated_diameter_max_km DESC LIMIT 5
        """,
        "5️⃣ Approaching in next 7 days": """
            SELECT a.name, ca.close_approach_date FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            WHERE ca.close_approach_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        """,
        "6️⃣ Total number of asteroids": """
            SELECT COUNT(*) AS total_asteroids FROM asteroids
        """,
        "7️⃣ Count: hazardous vs non-hazardous": """
            SELECT is_potentially_hazardous_asteroid, COUNT(*) AS count FROM asteroids
            GROUP BY is_potentially_hazardous_asteroid
        """,
        "8️⃣ Average velocity of all approaches": """
            SELECT AVG(relative_velocity_kmph) AS avg_velocity FROM close_approach
        """,
        "9️⃣ Closest asteroid ever": """
            SELECT a.name, ca.miss_distance_lunar FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            ORDER BY ca.miss_distance_lunar ASC LIMIT 1
        """,
        "🔟 Most frequent orbiting body": """
            SELECT orbiting_body, COUNT(*) AS count FROM close_approach
            GROUP BY orbiting_body ORDER BY count DESC LIMIT 1
        """,
        "1️⃣1️⃣ Asteroids with name starting 'A'": """
            SELECT * FROM asteroids WHERE name LIKE 'A%'
        """,
        "1️⃣2️⃣ Approaches between 0.1 - 0.3 AU": """
            SELECT a.name, ca.astronomical FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            WHERE ca.astronomical BETWEEN 0.1 AND 0.3
        """,
        "1️⃣3️⃣ Hazardous & diameter > 1 km": """
            SELECT * FROM asteroids
            WHERE is_potentially_hazardous_asteroid = TRUE AND estimated_diameter_max_km > 1
        """,
        "1️⃣4️⃣ Asteroids with speed > 100000 kmph": """
            SELECT a.name, ca.relative_velocity_kmph FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            WHERE ca.relative_velocity_kmph > 100000
        """,
        "1️⃣5️⃣ Upcoming approaches sorted by date": """
            SELECT a.name, ca.close_approach_date FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            WHERE ca.close_approach_date >= CURDATE()
            ORDER BY ca.close_approach_date ASC
        """,
        "1️⃣6️⃣ Velocity stats (avg, min, max)": """
            SELECT AVG(relative_velocity_kmph) AS avg_vel,
                   MIN(relative_velocity_kmph) AS min_vel,
                   MAX(relative_velocity_kmph) AS max_vel
            FROM close_approach
        """,
        "1️⃣7️⃣ Diameter between 0.5 - 1.5 km": """
            SELECT name, estimated_diameter_min_km, estimated_diameter_max_km
            FROM asteroids
            WHERE estimated_diameter_max_km BETWEEN 0.5 AND 1.5
        """,
        "1️⃣8️⃣ Asteroids with Earth as orbiting body": """
            SELECT a.name, ca.orbiting_body FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            WHERE ca.orbiting_body = 'Earth'
        """,
        "1️⃣9️⃣ Max velocity per orbiting body": """
            SELECT orbiting_body, MAX(relative_velocity_kmph) AS max_vel
            FROM close_approach
            GROUP BY orbiting_body
        """,
        "2️⃣0️⃣ Asteroids with duplicate names": """
            SELECT name, COUNT(*) as occurrences FROM asteroids
            GROUP BY name HAVING COUNT(*) > 1
        """
    }

    selected_query_label = st.selectbox("🧠 Select a predefined query", list(query_map.keys()))

    if selected_query_label:
        sql = query_map[selected_query_label]
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
            df = pd.DataFrame(rows, columns=cols)

            st.success(f"✅ Query Executed: {selected_query_label}")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")

# ✅ Close
cursor.close()
conn.close()