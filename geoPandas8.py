import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union

def create_universities_data():
    """Create synthetic university locations"""
    universities = {
        'University of Colombo': (79.86, 6.90),
        'University of Kelaniya': (79.92, 6.97),
        'University of Sri Jayewardenepura': (79.95, 6.85),
        'University of Peradeniya': (80.60, 7.25),
        'University of Ruhuna': (80.35, 6.08),
        'University of Jaffna': (80.03, 9.68),
        'Eastern University': (81.25, 8.55),
        'Rajarata University': (80.35, 8.35)
    }
    
    uni_data = []
    for name, coords in universities.items():
        uni_data.append({
            'name': name,
            'geometry': Point(coords),
            'type': 'National University',
            'student_capacity': np.random.randint(5000, 15000)
        })
    
    return gpd.GeoDataFrame(uni_data, crs="EPSG:4326")

def create_road_network():
    """Create synthetic major road network"""
    roads_data = [
        {
            'name': 'A1 Highway',
            'geometry': LineString([(79.85, 6.90), (80.00, 7.00), (80.60, 7.25), (80.80, 7.40)]),
            'type': 'Highway',
            'lanes': 4
        },
        {
            'name': 'A2 Highway', 
            'geometry': LineString([(79.85, 6.90), (80.20, 6.10), (80.35, 6.08)]),
            'type': 'Highway',
            'lanes': 4
        },
        {
            'name': 'A9 Highway',
            'geometry': LineString([(80.60, 7.25), (80.70, 7.80), (80.03, 9.68)]),
            'type': 'Highway', 
            'lanes': 2
        },
        {
            'name': 'A6 Highway',
            'geometry': LineString([(80.35, 8.35), (81.25, 8.55)]),
            'type': 'Highway',
            'lanes': 2
        },
        {
            'name': 'A4 Highway',
            'geometry': LineString([(80.20, 6.10), (81.10, 6.20)]),
            'type': 'Highway',
            'lanes': 2
        }
    ]
    
    return gpd.GeoDataFrame(roads_data, crs="EPSG:4326")

def create_districts_data():
    """Create synthetic district boundaries for Sri Lanka"""
    districts_data = [
        {
            'district': 'Colombo',
            'geometry': Polygon([(79.7, 6.7), (80.0, 6.7), (80.0, 7.1), (79.7, 7.1), (79.7, 6.7)]),
            'population_density': 2500,
            'youth_population': 450000
        },
        {
            'district': 'Gampaha',
            'geometry': Polygon([(79.9, 7.0), (80.2, 7.0), (80.2, 7.3), (79.9, 7.3), (79.9, 7.0)]),
            'population_density': 1800,
            'youth_population': 380000
        },
        {
            'district': 'Kandy',
            'geometry': Polygon([(80.4, 7.1), (80.8, 7.1), (80.8, 7.5), (80.4, 7.5), (80.4, 7.1)]),
            'population_density': 1200,
            'youth_population': 220000
        },
        {
            'district': 'Jaffna',
            'geometry': Polygon([(79.8, 9.5), (80.2, 9.5), (80.2, 9.9), (79.8, 9.9), (79.8, 9.5)]),
            'population_density': 800,
            'youth_population': 120000
        },
        {
            'district': 'Galle',
            'geometry': Polygon([(80.1, 5.9), (80.5, 5.9), (80.5, 6.3), (80.1, 6.3), (80.1, 5.9)]),
            'population_density': 950,
            'youth_population': 180000
        },
        {
            'district': 'Ampara',
            'geometry': Polygon([(81.0, 7.0), (81.5, 7.0), (81.5, 7.5), (81.0, 7.5), (81.0, 7.0)]),
            'population_density': 600,
            'youth_population': 90000
        },
        {
            'district': 'Badulla',
            'geometry': Polygon([(81.0, 6.5), (81.3, 6.5), (81.3, 7.0), (81.0, 7.0), (81.0, 6.5)]),
            'population_density': 400,
            'youth_population': 75000
        },
        {
            'district': 'Mannar',
            'geometry': Polygon([(79.7, 8.8), (80.0, 8.8), (80.0, 9.2), (79.7, 9.2), (79.7, 8.8)]),
            'population_density': 300,
            'youth_population': 50000
        },
        {
            'district': 'Monaragala',
            'geometry': Polygon([(81.2, 6.5), (81.6, 6.5), (81.6, 7.0), (81.2, 7.0), (81.2, 6.5)]),
            'population_density': 350,
            'youth_population': 60000
        }
    ]
    
    return gpd.GeoDataFrame(districts_data, crs="EPSG:4326")

# Create all datasets
print("Creating datasets...")
gdf_universities = create_universities_data()
gdf_roads = create_road_network()
gdf_districts = create_districts_data()

print("Datasets created successfully:")
print(f"Universities: {len(gdf_universities)}")
print(f"Roads: {len(gdf_roads)}")
print(f"Districts: {len(gdf_districts)}")

# Convert to a projected CRS for accurate buffer calculations (meters)
print("\nConverting to projected CRS...")
gdf_districts_utm = gdf_districts.to_crs("EPSG:5234")  # Sri Lanka UTM
gdf_universities_utm = gdf_universities.to_crs("EPSG:5234")
gdf_roads_utm = gdf_roads.to_crs("EPSG:5234")

# Create buffers around universities (30km service area)
print("Creating university buffers...")
university_buffers = gdf_universities_utm.copy()
university_buffers['geometry'] = university_buffers.geometry.buffer(30000)  # 30km buffer
university_buffers = university_buffers.to_crs("EPSG:4326")

# Create buffers around major roads (10km accessibility corridor)
print("Creating road buffers...")
road_buffers = gdf_roads_utm.copy()
road_buffers['geometry'] = road_buffers.geometry.buffer(10000)  # 10km buffer
road_buffers = road_buffers.to_crs("EPSG:4326")

# Combine all university service areas
print("\nCombining service areas...")
combined_university_service = gpd.GeoDataFrame(
    geometry=[unary_union(university_buffers.geometry)],
    crs="EPSG:4326"
)

# Combine all road accessibility corridors  
combined_road_corridors = gpd.GeoDataFrame(
    geometry=[unary_union(road_buffers.geometry)],
    crs="EPSG:4326"
)

# Identify areas served by universities (within any university buffer)
print("Analyzing district service coverage...")
gdf_districts['served_by_university'] = gdf_districts.geometry.apply(
    lambda x: combined_university_service.intersects(x).any()
)

# Identify areas with good road access (within any road buffer)
gdf_districts['good_road_access'] = gdf_districts.geometry.apply(
    lambda x: combined_road_corridors.intersects(x).any()
)

# Create a suitability score for new university locations
gdf_districts['suitability_score'] = (
    # Demand factors (positive)
    (gdf_districts['population_density'] / gdf_districts['population_density'].max()) * 0.3 +
    (gdf_districts['youth_population'] / gdf_districts['youth_population'].max()) * 0.3 +
    # Accessibility factors
    ((~gdf_districts['served_by_university']).astype(int) * 0.2) +
    (gdf_districts['good_road_access'].astype(int) * 0.2)
)

# Normalize suitability score to 0-1
gdf_districts['suitability_score'] = (
    gdf_districts['suitability_score'] / gdf_districts['suitability_score'].max()
)

# ============================================================================
# INTERACTIVE FOLIUM MAP CODE (CORRECTED)
# ============================================================================

print("\n" + "="*50)
print("CREATING INTERACTIVE FOLIUM MAP")
print("="*50)

# Create an interactive Folium map
suitability_map = folium.Map(location=[7.5, 80.5], zoom_start=7.5, tiles='OpenStreetMap')

# Add districts with suitability coloring
folium.GeoJson(
    gdf_districts,
    style_function=lambda feature: {
        'fillColor': plt.cm.RdYlGn(feature['properties']['suitability_score']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['district', 'suitability_score', 'population_density', 'youth_population'],
        aliases=['District:', 'Suitability Score:', 'Pop Density:', 'Youth Population:'],
        localize=True
    )
).add_to(suitability_map)

# Add university locations
for idx, row in gdf_universities.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"<b>{row['name']}</b><br>Type: {row['type']}",
        icon=folium.Icon(color='red', icon='university', prefix='fa')
    ).add_to(suitability_map)

# Add road network
for idx, row in gdf_roads.iterrows():
    folium.GeoJson(
        row.geometry,
        style_function=lambda x: {'color': 'orange', 'weight': 4}
    ).add_to(suitability_map)

# Add university service areas (CORRECTED - removed tooltip or fixed it)
folium.GeoJson(
    combined_university_service,
    style_function=lambda x: {'fillColor': 'blue', 'color': 'blue', 'fillOpacity': 0.2, 'weight': 2}
    # Removed the problematic tooltip that caused the error
).add_to(suitability_map)

# Add legend
legend_html = '''
<div style="position: fixed; 
     top: 10px; left: 50px; width: 250px; height: 200px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:14px; padding: 10px">
     <b>SRI LANKA UNIVERSITY PLANNING</b><br>
     <i class="fa fa-square" style="color:red"></i> Existing Universities<br>
     <i class="fa fa-square" style="color:orange"></i> Major Roads<br>
     <i class="fa fa-square" style="color:blue"></i> Service Areas<br>
     <br><b>Suitability:</b><br>
     <i class="fa fa-square" style="color:#d73027"></i> High<br>
     <i class="fa fa-square" style="color:#fee08b"></i> Medium<br>
     <i class="fa fa-square" style="color:#1a9850"></i> Low
</div>
'''
suitability_map.get_root().html.add_child(folium.Element(legend_html))

suitability_map.save('sri_lanka_university_suitability_map.html')
print("🗺️ Interactive map saved as 'sri_lanka_university_suitability_map.html'")

# Display the map (if running in Jupyter notebook)
try:
    display(suitability_map)
    print("Map displayed successfully!")
except:
    print("Map creation completed! Open 'sri_lanka_university_suitability_map.html' in your browser to view the interactive map.")