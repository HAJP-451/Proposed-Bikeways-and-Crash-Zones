#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  3 19:49:00 2025

@author: henrypaul
"""

# importing modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

# reading joined data
crash_and_prio = pd.read_csv('crash_and_prio.csv')

# reading old data
prop = pd.read_csv('Proposed_bikeways.csv')

# filtering data
crash_and_prio = crash_and_prio[['crash_count', 'PRIORITYRA']]

# proportion of crashes that are in high priority zones
tot_crashes = crash_and_prio['crash_count'].sum()
high_prio_crash  = crash_and_prio[crash_and_prio['PRIORITYRA'] <= 100]['crash_count'].sum()
low_prio_crash = crash_and_prio[crash_and_prio['PRIORITYRA'] > 100]['crash_count'].sum()

# plotting the proportion
fig, ax = plt.subplots()
labels = ['Accidents in High Priority Areas', 'Accidents in Low Priority Areas']
values = [high_prio_crash, low_prio_crash]
ax.pie(values, labels = labels, autopct='%1.2f%%')
fig.tight_layout()
fig.savefig('accidents_by_priority.png', bbox_inches='tight')

# regressing data
X = crash_and_prio['crash_count']
Y = crash_and_prio['PRIORITYRA']
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
print(model.summary())

# total cost of low-priority areas
hi_cost = prop[prop['PRIORITYRANK'] > 100]['HICOSTESTIMATE'].sum()
low_cost = prop[prop['PRIORITYRANK'] > 100]['LOWCOSTESTIMATE'].sum()
mean_cost = np.mean([hi_cost, low_cost])
print('High Cost Estimate:' + str(round(hi_cost,2)))
print("Low Cost Estimate:" + str(round(low_cost,2)))
print('Mean Cost Estimate:' + str(round(mean_cost, 2)))

# compare to total
hi_tot = prop['HICOSTESTIMATE'].sum()
lo_tot = prop['LOWCOSTESTIMATE'].sum()
mean_tot = np.mean([hi_tot, lo_tot])
hi_saved = hi_cost/hi_tot
lo_saved = low_cost/lo_tot
mean_saved = mean_cost/mean_tot
print("High Cost Savings as Fraction of Total Cost:", round(hi_saved, 2))
print("Low Cost Savings as Fraction of Total Cost:", round(lo_saved, 2))
print("Mean Cost Savings as Fraction of Total Cost:", round(mean_saved, 2))

# compare to highest-cost project
max_cost_index = prop['HICOSTESTIMATE'].idxmax()
max_cost_row = prop.loc[max_cost_index]
max_cost = max_cost_row['HICOSTESTIMATE']
print("Cost of Most Expensive Project:", round(max_cost,2))
max_v_saved = max_cost/hi_cost
print("As Fraction of Potential Savings:", round(max_v_saved, 2))
