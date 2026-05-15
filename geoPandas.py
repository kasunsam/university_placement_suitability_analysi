import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union
import folium
from folium import plugins

# Create synthetic Sri Lanka district boundaries (simplified)
def create_sri_lanka_districts():
    """Create simplified district boundaries for Sri Lanka"""
    districts_data = []
    
    # Simplified coordinates for major districts
    district_boundaries = {
        'Colombo': Polygon([(79.85, 6.9), (79.95, 6.9), (79.95, 7.0), (79.85, 7.0)]),
        'Gampaha': Polygon([(79.9, 7.0), (80.1, 7.0), (80.1, 7.2), (79.9, 7.2)]),
        'Kandy': Polygon([(80.6, 7.2), (80.8, 7.2), (80.8, 7.4), (80.6, 7.4)]),
        'Galle': Polygon([(80.2, 6.0), (80.4, 6.0), (80.4, 6.2), (80.2, 6.2)]),
        'Jaffna': Polygon([(80.0, 9.6), (80.2, 9.6), (80.2, 9.8), (80.0, 9.8)]),
        'Trincomalee': Polygon([(81.2, 8.5), (81.4, 8.5), (81.4, 8.7), (81.2, 8.7)]),
        'Anuradhapura': Polygon([(80.3, 8.3), (80.5, 8.3), (80.5, 8.5), (80.3, 8.5)]),
        'Badulla': Polygon([(81.0, 6.9), (81.2, 6.9), (81.2, 7.1), (81.0, 7.1)]),
        'Ratnapura': Polygon([(80.4, 6.7), (80.6, 6.7), (80.6, 6.9), (80.4, 6.9)]),
        'Hambantota': Polygon([(81.1, 6.1), (81.3, 6.1), (81.3, 6.3), (81.1, 6.3)])
    }
    
    # Population density data (persons per sq km)
    population_density = {
        'Colombo': 3500, 'Gampaha': 1800, 'Kandy': 1200, 'Galle': 800,
        'Jaffna': 600, 'Trincomalee': 300, 'Anuradhapura': 200,
        'Badulla': 400, 'Ratnapura': 350, 'Hambantota': 250
    }
    
    # Youth population percentage
    youth_population = {
        'Colombo': 25, 'Gampaha': 28, 'Kandy': 30, 'Galle': 26,
        'Jaffna': 32, 'Trincomalee': 35, 'Anuradhapura': 38,
        'Badulla': 33, 'Ratnapura': 31, 'Hambantota': 29
    }
    
    for district, geometry in district_boundaries.items():
        districts_data.append({
            'district': district,
            'geometry': geometry,
            'population_density': population_density[district],
            'youth_population': youth_population[district],
            'area_sq_km': geometry.area * 10000  # Rough approximation
        })
    
    return gpd.GeoDataFrame(districts_data, crs="EPSG:4326")

# Create the districts GeoDataFrame
gdf_districts = create_sri_lanka_districts()
print("Districts GeoDataFrame:")
print(gdf_districts.head())