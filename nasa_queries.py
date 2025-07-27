import mysql.connector

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Riya#2021",
    database="nasa_neo1"
)
cursor = conn.cursor()
print("✅ Connected to MySQL")

# 📄 20 SQL queries: 15 required + 5 extra
queries = [
    ("1️⃣ Count how many times each asteroid has approached Earth",
     """
     SELECT neo_reference_id, COUNT(*) AS approach_count
     FROM close_approach
     GROUP BY neo_reference_id
     ORDER BY approach_count DESC;
     """),

    ("2️⃣ Average velocity of each asteroid over multiple approaches",
     """
     SELECT neo_reference_id, AVG(relative_velocity_kmph) AS avg_velocity
     FROM close_approach
     GROUP BY neo_reference_id
     ORDER BY avg_velocity DESC;
     """),

    ("3️⃣ Top 10 fastest asteroids",
     """
     SELECT ca.neo_reference_id, a.name, MAX(ca.relative_velocity_kmph) AS max_speed
     FROM close_approach ca
     JOIN asteroids a ON ca.neo_reference_id = a.id
     GROUP BY ca.neo_reference_id, a.name
     ORDER BY max_speed DESC
     LIMIT 10;
     """),

    ("4️⃣ Hazardous asteroids that approached Earth more than 3 times",
     """
     SELECT ca.neo_reference_id, a.name, COUNT(*) AS approach_count
     FROM close_approach ca
     JOIN asteroids a ON ca.neo_reference_id = a.id
     WHERE a.is_potentially_hazardous_asteroid = TRUE
     GROUP BY ca.neo_reference_id, a.name
     HAVING approach_count > 3;
     """),

    ("5️⃣ Month with the most asteroid approaches",
     """
     SELECT MONTH(close_approach_date) AS month, COUNT(*) AS total_approaches
     FROM close_approach
     GROUP BY month
     ORDER BY total_approaches DESC;
     """),

    ("6️⃣ Asteroid with the fastest ever approach speed",
     """
     SELECT ca.neo_reference_id, a.name, ca.relative_velocity_kmph
     FROM close_approach ca
     JOIN asteroids a ON ca.neo_reference_id = a.id
     ORDER BY ca.relative_velocity_kmph DESC
     LIMIT 1;
     """),

    ("7️⃣ Sort asteroids by maximum estimated diameter (descending)",
     """
     SELECT id, name, estimated_diameter_max_km
     FROM asteroids
     ORDER BY estimated_diameter_max_km DESC;
     """),

    ("8️⃣ Asteroid whose closest approach is getting nearer over time",
     """
     SELECT neo_reference_id, close_approach_date, miss_distance_km
     FROM close_approach
     ORDER BY neo_reference_id, close_approach_date;
     """),

    ("9️⃣ Name, date, and miss distance of each asteroid’s closest approach",
     """
     SELECT a.name, ca.close_approach_date, MIN(ca.miss_distance_km) AS closest_approach
     FROM close_approach ca
     JOIN asteroids a ON ca.neo_reference_id = a.id
     GROUP BY ca.neo_reference_id, a.name;
     """),

    ("🔟 Asteroids that approached with velocity > 50,000 km/h",
     """
     SELECT ca.neo_reference_id, a.name, ca.relative_velocity_kmph
     FROM close_approach ca
     JOIN asteroids a ON ca.neo_reference_id = a.id
     WHERE ca.relative_velocity_kmph > 50000;
     """),

    ("1️⃣1️⃣ Count how many approaches happened per month",
     """
     SELECT MONTH(close_approach_date) AS month, COUNT(*) AS total_approaches
     FROM close_approach
     GROUP BY month
     ORDER BY month;
     """),

    ("1️⃣2️⃣ Asteroid with highest brightness (lowest magnitude)",
     """
     SELECT id, name, absolute_magnitude_h
     FROM asteroids
     ORDER BY absolute_magnitude_h ASC
     LIMIT 1;
     """),

    ("1️⃣3️⃣ Count of hazardous vs non-hazardous asteroids",
     """
     SELECT is_potentially_hazardous_asteroid, COUNT(*) AS total
     FROM asteroids
     GROUP BY is_potentially_hazardous_asteroid;
     """),

    ("1️⃣4️⃣ Asteroids that passed closer than the Moon (< 1 lunar distance)",
     """
     SELECT a.name, ca.close_approach_date, ca.miss_distance_lunar
     FROM close_approach ca
     JOIN asteroids a ON ca.neo_reference_id = a.id
     WHERE ca.miss_distance_lunar < 1;
     """),

    ("1️⃣5️⃣ Asteroids that came within 0.05 AU",
     """
     SELECT a.name, ca.close_approach_date, ca.astronomical
     FROM close_approach ca
     JOIN asteroids a ON ca.neo_reference_id = a.id
     WHERE ca.astronomical < 0.05;
     """),

    # 🔥 EXTRA CUSTOM QUERIES BELOW:

    ("1️⃣6️⃣ Orbiting body with most asteroid approaches",
     """
     SELECT orbiting_body, COUNT(*) AS total_approaches
     FROM close_approach
     GROUP BY orbiting_body
     ORDER BY total_approaches DESC;
     """),

    ("1️⃣7️⃣ Top 5 asteroids with widest size range",
     """
     SELECT id, name,
     (estimated_diameter_max_km - estimated_diameter_min_km) AS size_range
     FROM asteroids
     ORDER BY size_range DESC
     LIMIT 5;
     """),

    ("1️⃣8️⃣ Number of approaches per year",
     """
     SELECT YEAR(close_approach_date) AS year, COUNT(*) AS total
     FROM close_approach
     GROUP BY year
     ORDER BY year;
     """),

    ("1️⃣9️⃣ Fastest average velocity by orbiting body",
     """
     SELECT orbiting_body, AVG(relative_velocity_kmph) AS avg_speed
     FROM close_approach
     GROUP BY orbiting_body
     ORDER BY avg_speed DESC;
     """),

    ("2️⃣0️⃣ Day with the most asteroid visits",
     """
     SELECT close_approach_date, COUNT(*) AS total
     FROM close_approach
     GROUP BY close_approach_date
     ORDER BY total DESC
     LIMIT 1;
     """)
]

# 🔁 Run each query and print results
for label, sql in queries:
    print(f"\n==============================")
    print(f"🔍 {label}")
    print("==============================")
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows[:10]:  # print only first 10 rows for preview
        print(row)

conn.close()
print("\n✅ All queries executed successfully!")