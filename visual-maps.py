import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union
from matplotlib.patches import Patch, Circle

# Create the datasets
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

# Convert to projected CRS and create buffers
print("\nConverting to projected CRS and creating buffers...")
gdf_districts_utm = gdf_districts.to_crs("EPSG:5234")
gdf_universities_utm = gdf_universities.to_crs("EPSG:5234")
gdf_roads_utm = gdf_roads.to_crs("EPSG:5234")

# Create university buffers (30km service area)
university_buffers = gdf_universities_utm.copy()
university_buffers['geometry'] = university_buffers.geometry.buffer(30000)
university_buffers = university_buffers.to_crs("EPSG:4326")

# Create road buffers (10km accessibility corridor)
road_buffers = gdf_roads_utm.copy()
road_buffers['geometry'] = road_buffers.geometry.buffer(10000)
road_buffers = road_buffers.to_crs("EPSG:4326")

# Combine service areas
combined_university_service = gpd.GeoDataFrame(
    geometry=[unary_union(university_buffers.geometry)],
    crs="EPSG:4326"
)

# Combine road corridors
combined_road_corridors = gpd.GeoDataFrame(
    geometry=[unary_union(road_buffers.geometry)],
    crs="EPSG:4326"
)

# Analyze service coverage
print("Analyzing service coverage...")
gdf_districts['served_by_university'] = gdf_districts.geometry.apply(
    lambda x: combined_university_service.intersects(x).any()
)

# Analyze road access
gdf_districts['good_road_access'] = gdf_districts.geometry.apply(
    lambda x: combined_road_corridors.intersects(x).any()
)

print(f"\nService Coverage Analysis:")
print(f"Districts with university access: {gdf_districts['served_by_university'].sum()}")
print(f"Districts with good road access: {gdf_districts['good_road_access'].sum()}")

# Calculate suitability scores
print("Calculating suitability scores...")
gdf_districts['suitability_score'] = (
    (gdf_districts['population_density'] / gdf_districts['population_density'].max()) * 0.3 +
    (gdf_districts['youth_population'] / gdf_districts['youth_population'].max()) * 0.3 +
    ((~gdf_districts['served_by_university']).astype(int) * 0.2) +
    (gdf_districts['good_road_access'].astype(int) * 0.2)
)

# Normalize scores
gdf_districts['suitability_score'] = gdf_districts['suitability_score'] / gdf_districts['suitability_score'].max()
gdf_districts['suitability_rank'] = gdf_districts['suitability_score'].rank(ascending=False)

print("Suitability scores calculated successfully!")

# ============================================================================
# MAP 1: Population Demand Heatmap with Existing Infrastructure
# ============================================================================

print("\n" + "="*60)
print("CREATING MAP 1: Population Demand Heatmap")
print("="*60)

fig, ax = plt.subplots(1, 1, figsize=(15, 12))

# Create population density heatmap
gdf_districts.plot(column='population_density', ax=ax, 
                   cmap='YlOrRd', edgecolor='black', legend=True,
                   legend_kwds={'label': 'Population Density (people/sq km)', 
                               'orientation': 'horizontal', 'shrink': 0.8})

# Add existing universities
gdf_universities.plot(ax=ax, color='blue', markersize=150, marker='^', 
                      edgecolor='white', linewidth=2, label='Existing Universities')

# Add road network
gdf_roads.plot(ax=ax, color='darkgreen', linewidth=3, label='Major Highways')

# Add district labels with population information
for idx, row in gdf_districts.iterrows():
    ax.annotate(text=f"{row['district']}\n({row['population_density']} pop/km²)", 
                xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                xytext=(5, 5), textcoords="offset points",
                fontsize=9, fontweight='bold', alpha=0.8,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))

ax.set_title('Sri Lanka: Population Density Heatmap with Educational Infrastructure', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper left')
ax.set_axis_off()
plt.tight_layout()
plt.show()