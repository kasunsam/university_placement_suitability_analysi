import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
# MAP VISUALIZATION CODE
# ============================================================================

print("\n" + "="*50)
print("GENERATING MAP VISUALIZATIONS")
print("="*50)

# Create a comprehensive map visualization
fig, axes = plt.subplots(2, 2, figsize=(20, 16))

# Plot 1: Base map with districts and universities
gdf_districts.plot(ax=axes[0,0], color='lightgray', edgecolor='black', alpha=0.7)
gdf_universities.plot(ax=axes[0,0], color='red', markersize=100, marker='^', label='Universities')
gdf_roads.plot(ax=axes[0,0], color='orange', linewidth=2, label='Major Roads')
axes[0,0].set_title('Sri Lanka: Universities and Major Road Network', fontsize=14, fontweight='bold')
axes[0,0].legend()

# Plot 2: University service areas
gdf_districts.plot(ax=axes[0,1], color='lightgray', edgecolor='black', alpha=0.7)
university_buffers.plot(ax=axes[0,1], color='blue', alpha=0.3, label='30km Service Area')
gdf_universities.plot(ax=axes[0,1], color='red', markersize=100, marker='^')
axes[0,1].set_title('University Service Areas (30km radius)', fontsize=14, fontweight='bold')
axes[0,1].legend()

# Plot 3: Road accessibility corridors
gdf_districts.plot(ax=axes[1,0], color='lightgray', edgecolor='black', alpha=0.7)
road_buffers.plot(ax=axes[1,0], color='green', alpha=0.3, label='10km Road Corridor')
gdf_roads.plot(ax=axes[1,0], color='orange', linewidth=2)
axes[1,0].set_title('Road Accessibility Corridors (10km radius)', fontsize=14, fontweight='bold')
axes[1,0].legend()

# Plot 4: Suitability map
gdf_districts.plot(column='suitability_score', ax=axes[1,1], 
                   cmap='RdYlGn', edgecolor='black', legend=True,
                   legend_kwds={'label': 'Suitability Score', 'orientation': 'horizontal'})
gdf_universities.plot(ax=axes[1,1], color='red', markersize=80, marker='^', label='Existing Universities')
axes[1,1].set_title('University Placement Suitability Map', fontsize=14, fontweight='bold')

# Add district labels
for idx, row in gdf_districts.iterrows():
    axes[1,1].annotate(text=row['district'], 
                      xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                      xytext=(3, 3), textcoords="offset points",
                      fontsize=8, alpha=0.8)

axes[1,1].legend()

plt.tight_layout()
plt.show()

print("Map visualization completed successfully!")