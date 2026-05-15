import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union
from matplotlib.patches import Patch, Circle

print("\n" + "="*60)
print("CREATING MAP 2: Infrastructure & Service Gaps Analysis")
print("="*60)

# Create all necessary datasets first
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

# Create datasets
gdf_universities = create_universities_data()
gdf_roads = create_road_network()
gdf_districts = create_districts_data()

# Convert to projected CRS and create buffers
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

# Analyze service coverage
gdf_districts['served_by_university'] = gdf_districts.geometry.apply(
    lambda x: university_buffers.unary_union.intersects(x) if hasattr(university_buffers, 'unary_union') else unary_union(university_buffers.geometry).intersects(x)
)

# Create the visualization
fig, ax = plt.subplots(1, 1, figsize=(15, 12))

# Base districts with service status coloring
gdf_districts['service_status'] = gdf_districts['served_by_university'].map({
    True: 'Served', 
    False: 'Unserved'
})

colors = {'Served': 'lightgreen', 'Unserved': 'lightcoral'}
gdf_districts.plot(ax=ax, color=gdf_districts['service_status'].map(colors), 
                   edgecolor='black', linewidth=1)

# Add university service areas (30km buffers)
university_buffers.plot(ax=ax, color='blue', alpha=0.3, 
                       label='30km University Service Area')

# Add road accessibility corridors (10km buffers)
road_buffers.plot(ax=ax, color='orange', alpha=0.3, 
                 label='10km Road Accessibility Corridor')

# Add infrastructure layers
gdf_universities.plot(ax=ax, color='darkblue', markersize=100, marker='^', 
                     label='Universities')
gdf_roads.plot(ax=ax, color='darkorange', linewidth=2, label='Highways')

# Highlight completely underserved districts (no university access)
underserved_districts = gdf_districts[~gdf_districts['served_by_university']]
if not underserved_districts.empty:
    underserved_districts.plot(ax=ax, color='red', edgecolor='darkred', 
                              linewidth=2, alpha=0.5, label='Underserved Districts')

    # Add detailed labels for underserved areas
    for idx, row in underserved_districts.iterrows():
        ax.annotate(text=f"🚨 {row['district']}\nNo University Access", 
                    xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                    xytext=(10, 10), textcoords="offset points",
                    fontsize=10, fontweight='bold', color='darkred',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

ax.set_title('Infrastructure Accessibility & Educational Service Gaps Analysis', 
             fontsize=16, fontweight='bold', pad=20)

# Create custom legend
legend_elements = [
    Patch(facecolor='lightgreen', label='Districts with University Access'),
    Patch(facecolor='lightcoral', label='Districts without University Access'),
    Patch(facecolor='red', alpha=0.5, label='Underserved Districts'),
    Patch(facecolor='blue', alpha=0.3, label='University Service Area (30km)'),
    Patch(facecolor='orange', alpha=0.3, label='Road Accessibility (10km)')
]
ax.legend(handles=legend_elements, loc='upper left')

ax.set_axis_off()
plt.tight_layout()
plt.show()

print("Map 2 created successfully!")