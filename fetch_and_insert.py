import requests
import mysql.connector

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Riya#2021",  
    database="nasa_neo1"
)
cursor = conn.cursor()
print("✅ Connected to MySQL")

# Step 2: Fetch data from NASA API
url = "https://api.nasa.gov/neo/rest/v1/feed"
params = {
    "start_date": "2024-01-01",
    "end_date": "2024-01-03",
    "api_key": "JVeffAVg2AB1DXxxYzY7JWzuaAO2LDxtEXJNBFz4" 
}

response = requests.get(url, params=params)
data = response.json()

# Step 3: Extract and insert
for date in data["near_earth_objects"]:
    for asteroid in data["near_earth_objects"][date]:
        # Insert into asteroids table
        asteroid_insert = """
            INSERT IGNORE INTO asteroids (
                id, name, absolute_magnitude_h,
                estimated_diameter_min_km,
                estimated_diameter_max_km,
                is_potentially_hazardous_asteroid
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        est_dia = asteroid["estimated_diameter"]["kilometers"]
        cursor.execute(asteroid_insert, (
            int(asteroid["id"]),
            asteroid["name"],
            asteroid["absolute_magnitude_h"],
            est_dia["estimated_diameter_min"],
            est_dia["estimated_diameter_max"],
            asteroid["is_potentially_hazardous_asteroid"]
        ))

        # Insert into close_approach table
        for approach in asteroid["close_approach_data"]:
            approach_insert = """
                INSERT INTO close_approach (
                    neo_reference_id,
                    close_approach_date,
                    relative_velocity_kmph,
                    astronomical,
                    miss_distance_km,
                    miss_distance_lunar,
                    orbiting_body
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            miss = approach["miss_distance"]
            vel = approach["relative_velocity"]
            cursor.execute(approach_insert, (
                int(asteroid["id"]),
                approach["close_approach_date"],
                float(vel["kilometers_per_hour"]),
                float(miss["astronomical"]),
                float(miss["kilometers"]),
                float(miss["lunar"]),
                approach["orbiting_body"]
            ))

conn.commit()
print("✅ Data inserted successfully!")

cursor.close()
conn.close()