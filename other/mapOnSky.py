from skyfield.api import load, Topos, Observer

# Load the ephemeris data
planets = load('de421.bsp')

# Set the observer location (e.g., latitude, longitude, altitude)
observer = Observer(lat=40.0, lon=-75.0)

# Get the position of Mars at a specific time
ts = load.timescale()
t = ts.utc(2024, 1, 12, 20, 0, 0)
mars = planets['Mars']

# Calculate the apparent position of Mars from the observer's perspective
apparent_mars = observer.at(t).observe(mars)

# Get the altitude and azimuth
alt = apparent_mars.alt
az = apparent_mars.az

# Display the altitude and azimuth
print(f"Mars will be at altitude {alt.degrees:.2f} degrees and azimuth {az.degrees:.2f} degrees.")
