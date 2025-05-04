#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 20:40:33 2025

@author: henrypaul
"""

# importing modules
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# reading csv data
crash = pd.read_csv('Crash_Locations_Last_Five_Years.csv')
prop = pd.read_csv('Proposed_bikeways.csv')

# reading geodata
crash_geo = gpd.read_file('Crash_Locations_Last_Five_Years.zip')
prop_geo = gpd.read_file('Proposed_Bikeways.zip')
road_geo = gpd.read_file('tl_2020_06085_roads.zip')
limits_geo = gpd.read_file('City_Limits.zip')

# dropping crash records that don't have bicycle
tot_acc = len(crash_geo)
crash_geo = crash_geo.dropna(subset = 'VEHICLEPAR')
crash_bike = crash_geo[crash_geo['VEHICLEPAR'].str.contains('Bicycle')]

# plotting portion that have bikes versus portion that doesn't
fig, ax = plt.subplots()
bike_acc = len(crash_bike)
no_bike_acc = tot_acc - bike_acc
labels = ['Bike Accidents', 'Bikeless Accidents']
values = [bike_acc, no_bike_acc]
ax.pie(values, labels = labels, autopct='%1.2f%%')
fig.tight_layout()
fig.savefig('bike_accident_proportion.png')

# grouping bike crashes by year
fig, ax = plt.subplots()
bike_by_year = crash_bike['YEAR'].value_counts().sort_index().reset_index()
ax.bar(bike_by_year['YEAR'], bike_by_year['count'])
ax.set_xlabel('Year')
ax.set_ylabel('Number of Bike Accidents')
fig.tight_layout()
fig.savefig('bike_accidents_yearly.png')

# setting crs
road_geo = road_geo.to_crs("EPSG:4326")
limits_geo = limits_geo.to_crs("EPSG:4326")


# overlaying roads onto city limits
city_roads = gpd.overlay(road_geo, limits_geo, how = 'intersection', keep_geom_type = True)

# joining bike crashes to city roads
crash_bike = crash_bike.to_crs(city_roads.crs)
bike_on_road = gpd.sjoin_nearest(crash_bike, city_roads, how="left", distance_col="dist")
crash_per_road = bike_on_road.groupby("index_right").size().reset_index(name="crash_count")
city_roads["crash_count"] = city_roads.index.map(crash_per_road.set_index("index_right")["crash_count"])
city_roads["crash_count"] = city_roads["crash_count"].fillna(0)

# exporting a testing gpkg
crash_bike.to_file('bike_test.gpkg', layer = 'crash')
limits_geo.to_file('limits_test.gpkg', layer = 'limit')
city_roads.to_file('city_road_test.gpkg', layer = 'city roads')
prop_geo.to_file('prop_test.gpkg', layer = 'bikeways')

