import requests
import mysql.connector
import time

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Riya#2021",
    database="nasa_neo1"
)
cursor = conn.cursor()
print("✅ Connected to MySQL")

# Your personal API key
API_KEY = "JVeffAVg2AB1DXxxYzY7JWzuaAO2LDxtEXJNBFz4"

# Prepare insert query
insert_query = """
INSERT INTO close_approach (
    neo_reference_id,
    close_approach_date,
    relative_velocity_kmph,
    astronomical,
    miss_distance_km,
    miss_distance_lunar,
    orbiting_body
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

MAX_RECORDS = 10000
count = 0
skipped = 0
page = 0

while count < MAX_RECORDS:
    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?page={page}&api_key={API_KEY}"
    print(f"📡 Fetching page {page}...")
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ API error. Stopping.")
        break

    data = response.json()
    asteroids = data['near_earth_objects']

    if not asteroids:
        print("✅ All pages fetched.")
        break

    for asteroid in asteroids:
        neo_id = int(asteroid['id'])

        for approach in asteroid['close_approach_data']:
            if count >= MAX_RECORDS:
                break

            try:
                if (
                    'close_approach_date' in approach and
                    'relative_velocity' in approach and 'kilometers_per_hour' in approach['relative_velocity'] and
                    'miss_distance' in approach and
                    'astronomical' in approach['miss_distance'] and
                    'kilometers' in approach['miss_distance'] and
                    'lunar' in approach['miss_distance'] and
                    'orbiting_body' in approach
                ):
                    close_date = approach['close_approach_date']
                    velocity = float(approach['relative_velocity']['kilometers_per_hour'])
                    astronomical = float(approach['miss_distance']['astronomical'])
                    miss_km = float(approach['miss_distance']['kilometers'])
                    miss_lunar = float(approach['miss_distance']['lunar'])
                    orbiting_body = approach['orbiting_body']

                    values = (neo_id, close_date, velocity, astronomical, miss_km, miss_lunar, orbiting_body)
                    cursor.execute(insert_query, values)
                    count += 1
                else:
                    skipped += 1
                    continue

            except Exception as e:
                skipped += 1
                continue

    if count >= MAX_RECORDS:
        break

    conn.commit()
    page += 1
    time.sleep(1)

print(f"\n✅ Total inserted: {count}")
print(f"❌ Total skipped: {skipped}")
conn.close()