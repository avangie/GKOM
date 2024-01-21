import requests
import json

def get_planet_position(planet_name, observer_location, date_time):
    # Specify the Horizons Ephemeris Service URL
    base_url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    # Set up the parameters for the request
    query_params = {
        "target": f"{planet_name}",
        "observer": f"{observer_location}",
        "center": "399",  # Earth
        "utc": True,
        "date_format": "isot",
        "start_time": f"{date_time}T00:00:00.000",
        "stop_time": f"{date_time}T23:59:59.999",
        "id": "100",  # Ephemeris type (100 = Astronomical)
    }

    # Make the HTTP request
    response = requests.get(base_url, params=query_params)

    # Check if the response is successful
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data: {response.status_code}")

    # Parse the JSON response
    response_data = json.loads(response.text)

    # Extract the planet's location
    planet_location = response_data["orbital_elements"]["position"]
    right_ascension = planet_location["ra"]
    declination = planet_location["dec"]

    # Return the planet's location
    return f"Right Ascension: {right_ascension}, Declination: {declination}"

# Example usage
planet_name = "Mars"
observer_location = "500"  # Observer location (500 corresponds to Earth)
date_time = "2024-01-12"

try:
    planet_position = get_planet_position(planet_name, observer_location, date_time)
    print(planet_position)
except (ValueError, KeyError) as e:
    print(f"Error: {e}")
