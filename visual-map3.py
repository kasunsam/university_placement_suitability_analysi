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
# MAP 3: Final Suitability Analysis & Priority Recommendations
# ============================================================================

print("\n" + "="*60)
print("CREATING MAP 3: Suitability Analysis & Recommendations")
print("="*60)

fig, ax = plt.subplots(1, 1, figsize=(15, 12))

# Create suitability heatmap with discrete color bins
bins = [0, 0.3, 0.5, 0.7, 1.0]
labels = ['Low', 'Medium-Low', 'Medium-High', 'High']
gdf_districts['suitability_category'] = pd.cut(gdf_districts['suitability_score'], 
                                             bins=bins, labels=labels)

# Plot with categorical colors
colors = {'Low': 'red', 'Medium-Low': 'orange', 'Medium-High': 'yellow', 'High': 'green'}
gdf_districts.plot(ax=ax, color=gdf_districts['suitability_category'].map(colors), 
                   edgecolor='black', linewidth=1.5)

# Add existing infrastructure
gdf_universities.plot(ax=ax, color='darkblue', markersize=120, marker='^', 
                     edgecolor='white', linewidth=2, label='Existing Universities')
gdf_roads.plot(ax=ax, color='gray', linewidth=1.5, alpha=0.7, label='Road Network')

# Highlight top 3 recommendations with different markers
top_3 = gdf_districts.nlargest(3, 'suitability_score')
for i, (idx, district) in enumerate(top_3.iterrows()):
    color = ['gold', 'silver', 'brown'][i]
    marker = ['*', 'D', 's'][i]
    size = [400, 300, 200][i]
    
    # Plot recommendation markers
    ax.scatter(x=district.geometry.centroid.x, 
               y=district.geometry.centroid.y, 
               color=color, marker=marker, s=size, 
               edgecolor='black', linewidth=2, 
               zorder=5, label=f'Recommendation #{i+1}')

# Add detailed annotation for each district
for idx, row in gdf_districts.iterrows():
    rank = int(row['suitability_rank'])
    score = row['suitability_score']
    
    ax.annotate(text=f"{row['district']}\nRank: {rank}\nScore: {score:.3f}", 
                xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                xytext=(8, 8), textcoords="offset points",
                fontsize=8, fontweight='normal',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Special emphasis on Ampara (primary recommendation)
ampara = gdf_districts[gdf_districts['district'] == 'Ampara'].iloc[0]
ax.annotate(text=f"🏆 PRIMARY RECOMMENDATION: Ampara\n"
                 f"Suitability Score: {ampara['suitability_score']:.3f}\n"
                 f"Youth Population: {ampara['youth_population']:,}\n"
                 f"Service Gap: {'YES' if not ampara['served_by_university'] else 'NO'}", 
            xy=(ampara.geometry.centroid.x, ampara.geometry.centroid.y),
            xytext=(20, 20), textcoords="offset points",
            fontsize=10, fontweight='bold', color='darkred',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='gold', alpha=0.9),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))

ax.set_title('University Placement Suitability Analysis: Final Recommendations', 
             fontsize=16, fontweight='bold', pad=20)

# Create comprehensive legend
legend_elements = [
    Patch(facecolor='green', label='High Suitability (0.7-1.0)'),
    Patch(facecolor='yellow', label='Medium-High Suitability (0.5-0.7)'),
    Patch(facecolor='orange', label='Medium-Low Suitability (0.3-0.5)'),
    Patch(facecolor='red', label='Low Suitability (0.0-0.3)'),
    Circle((0,0), radius=1, color='darkblue', label='Existing Universities'),
    Circle((0,0), radius=1, color='gold', label='Recommendation #1 (Ampara)'),
    Circle((0,0), radius=1, color='silver', label='Recommendation #2'),
    Circle((0,0), radius=1, color='brown', label='Recommendation #3')
]

ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
ax.set_axis_off()
plt.tight_layout()
plt.show()

# Print summary statistics
print("🎯 SUITABILITY ANALYSIS SUMMARY")
print("="*50)
for category in labels:
    count = len(gdf_districts[gdf_districts['suitability_category'] == category])
    print(f"{category} Suitability: {count} districts")

print(f"\n🏆 TOP 3 RECOMMENDED DISTRICTS:")
top_3_sorted = top_3.sort_values('suitability_rank')
for i, (idx, district) in enumerate(top_3_sorted.iterrows()):
    served_status = "Served" if district['served_by_university'] else "Unserved"
    road_status = "Good Road Access" if district['good_road_access'] else "Poor Road Access"
    print(f"{i+1}. {district['district']} (Score: {district['suitability_score']:.3f}, {served_status}, {road_status})")

print(f"\n📊 MAP CREATION COMPLETED SUCCESSFULLY!")