import mysql.connector
import requests

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Riya#2021",
        database="nasa_neo1"
    )
    print("✅ Connected to MySQL")

    cursor = conn.cursor()

    # Fetch asteroid data from NASA API
    url = "https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=JVeffAVg2AB1DXxxYzY7JWzuaAO2LDxtEXJNBFz4"
    response = requests.get(url)
    data = response.json()
    asteroids = data['near_earth_objects']

    # Insert asteroid data
    insert_query = """
    INSERT INTO asteroids (id, name, absolute_magnitude_h, estimated_diameter_min_km, estimated_diameter_max_km, is_potentially_hazardous_asteroid)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for asteroid in asteroids:
        asteroid_id = int(asteroid['id'])
        name = asteroid['name']
        absolute_magnitude_h = asteroid['absolute_magnitude_h']
        min_diameter = asteroid['estimated_diameter']['kilometers']['estimated_diameter_min']
        max_diameter = asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']
        is_hazardous = asteroid['is_potentially_hazardous_asteroid']

        cursor.execute(insert_query, (
            asteroid_id,
            name,
            absolute_magnitude_h,
            min_diameter,
            max_diameter,
            is_hazardous
        ))

    conn.commit()
    print("✅ Asteroid data inserted successfully!")

except mysql.connector.Error as err:
    print("❌ Connection or Insert Failed:")
    print(err)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()