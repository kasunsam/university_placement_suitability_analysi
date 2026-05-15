import geopandas as gpd
import numpy as np
import pandas as pd
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

print("\nUniversity Buffer Analysis:")
print(f"Number of university service areas: {len(university_buffers)}")
print(f"Total area covered by university buffers: {university_buffers.to_crs('EPSG:5234').geometry.area.sum() / 1e6:.0f} sq km")

print("\nRoad Buffer Analysis:")
print(f"Number of road corridors: {len(road_buffers)}")
print(f"Total area covered by road buffers: {road_buffers.to_crs('EPSG:5234').geometry.area.sum() / 1e6:.0f} sq km")

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

print("\nDistrict Service Analysis:")
service_summary = gdf_districts.groupby('served_by_university').agg({
    'district': 'count',
    'population_density': 'mean',
    'youth_population': 'mean'
}).round(2)
print(service_summary)

# Calculate percentage of population served
total_population_served = gdf_districts[gdf_districts['served_by_university']]['population_density'].sum()
total_population = gdf_districts['population_density'].sum()
coverage_percentage = (total_population_served / total_population) * 100

print(f"\n📊 Population Coverage Analysis:")
print(f"Total population (density-weighted): {total_population:.0f}")
print(f"Population served by universities: {total_population_served:.0f}")
print(f"Coverage percentage: {coverage_percentage:.1f}%")

# Additional analysis
print(f"\n📈 Additional Insights:")
print(f"Districts with university access: {gdf_districts['served_by_university'].sum()} out of {len(gdf_districts)}")
print(f"Districts with good road access: {gdf_districts['good_road_access'].sum()} out of {len(gdf_districts)}")

# Districts without university access
unserved_districts = gdf_districts[~gdf_districts['served_by_university']]['district'].tolist()
print(f"Districts without university access: {unserved_districts}")

# Identify underserved districts (no university service AND low road access)
gdf_districts['underserved'] = (~gdf_districts['served_by_university']) & (~gdf_districts['good_road_access'])

# Calculate underserved population
underserved_population = gdf_districts[gdf_districts['underserved']]['population_density'].sum()
underserved_youth = gdf_districts[gdf_districts['underserved']]['youth_population'].mean()

print("\n🚨 UNDERSERVED AREAS ANALYSIS:")
print("="*50)
underserved_districts = gdf_districts[gdf_districts['underserved']]
if len(underserved_districts) > 0:
    print("Underserved Districts:")
    for idx, row in underserved_districts.iterrows():
        print(f"  • {row['district']}: Pop density: {row['population_density']}, Youth: {row['youth_population']}")
    print(f"\nTotal underserved population (density): {underserved_population:.0f}")
    print(f"Average youth population in underserved areas: {underserved_youth:.0f}")
else:
    print("No completely underserved districts found (all have some university or road access)")

# Create a more nuanced underserved score
gdf_districts['underserved_score'] = (
    # High population density increases need
    (gdf_districts['population_density'] / gdf_districts['population_density'].max()) * 0.4 +
    # High youth population increases need  
    (gdf_districts['youth_population'] / gdf_districts['youth_population'].max()) * 0.4 -
    # Existing service reduces need
    (gdf_districts['served_by_university'].astype(int)) * 0.2
)

# Rank districts by underserved score
gdf_districts['underserved_rank'] = gdf_districts['underserved_score'].rank(ascending=False)

print("\n📋 DISTRICT RANKING BY UNDERSERVED SCORE:")
print("="*50)
top_underserved = gdf_districts.nlargest(5, 'underserved_score')[['district', 'underserved_score', 'underserved_rank', 'population_density', 'youth_population']]
print(top_underserved.to_string(index=False))

# ============================================================================
# SUITABILITY ANALYSIS FOR NEW UNIVERSITY LOCATIONS
# ============================================================================

print("\n" + "="*60)
print("SUITABILITY ANALYSIS FOR NEW UNIVERSITY LOCATIONS")
print("="*60)

# Create a suitability score for new university locations
gdf_districts['suitability_score'] = (
    # Demand factors (positive)
    (gdf_districts['population_density'] / gdf_districts['population_density'].max()) * 0.3 +
    (gdf_districts['youth_population'] / gdf_districts['youth_population'].max()) * 0.3 +
    # Accessibility penalty (negative - prefer areas with some but not full access)
    ((~gdf_districts['served_by_university']).astype(int) * 0.2) +
    (gdf_districts['good_road_access'].astype(int) * 0.2)
)

# Normalize suitability score to 0-1
gdf_districts['suitability_score'] = (
    gdf_districts['suitability_score'] / gdf_districts['suitability_score'].max()
)

# Rank districts by suitability
gdf_districts['suitability_rank'] = gdf_districts['suitability_score'].rank(ascending=False)

print("🏆 TOP SUITABLE LOCATIONS FOR NEW UNIVERSITY:")
print("="*50)
top_suitable = gdf_districts.nlargest(5, 'suitability_score')[[
    'district', 'suitability_score', 'suitability_rank', 
    'population_density', 'youth_population', 'served_by_university'
]]
print(top_suitable.to_string(index=False))

# Detailed explanation of the suitability analysis
print("\n📊 SUITABILITY SCORE EXPLANATION:")
print("="*50)
print("The suitability score is calculated based on:")
print("• 30% - Population density (higher = more demand)")
print("• 30% - Youth population (higher = more potential students)")
print("• 20% - Not currently served by university (priority for underserved areas)")
print("• 20% - Good road access (infrastructure advantage)")
print("\nScores are normalized to 0-1 scale for comparison")

# Show all districts with their suitability scores
print("\n📋 ALL DISTRICTS SUITABILITY RANKING:")
print("="*50)
all_districts_ranked = gdf_districts.sort_values('suitability_rank')[[
    'district', 'suitability_score', 'suitability_rank', 
    'population_density', 'youth_population', 'served_by_university', 'good_road_access'
]]
print(all_districts_ranked.to_string(index=False))

# Final recommendation
print("\n🎯 RECOMMENDATION FOR NEW UNIVERSITY LOCATION:")
print("="*50)
best_location = top_suitable.iloc[0]
print(f"📍 PRIMARY RECOMMENDATION: {best_location['district']}")
print(f"   • Suitability Score: {best_location['suitability_score']:.3f}")
print(f"   • Population Density: {best_location['population_density']}")
print(f"   • Youth Population: {best_location['youth_population']:,}")
print(f"   • Currently Served by University: {'Yes' if best_location['served_by_university'] else 'No'}")

# Alternative recommendations
print(f"\n📍 ALTERNATIVE LOCATIONS:")
for i in range(1, min(3, len(top_suitable))):
    alt_location = top_suitable.iloc[i]
    print(f"   {i+1}. {alt_location['district']} (Score: {alt_location['suitability_score']:.3f})")