# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: chf
#     language: python
#     name: python3
# ---

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_finscope_path, load_finscope_data, load_finscope_sav

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)  

# ### Overview
#
# The script creates a standardized time series of the share of South Africans who are members of a burial society, have funeral insurance, and have life insurance from 2006 to 2019 using FinScope data. 
#
# A significant challenge in this process is the evolution of the FinScope survey questionnaire over time, with three different survey providers used. The questions and their corresponding variable names, as well as the response codes for `"have now"` or `"have it in my name"`, change from year to year. The script addresses this by manually identifying the correct variable and response code for each year and creating a consistent indicator variable (e.g., `burial_society_ind`) for each type of insurance product. For instance, the indicator for having a burial society is defined by `df06.Q67AP == 3` in 2006, while it is `df11.Q56_9 == 2` in 2011 and `df19.i1_10 == 3` in 2019.
#
# The script creates a single funeral insurance indicator by checking if a respondent has any of the different types of funeral insurance listed in a given year. For example, in the 2006 data, the funeral insurance indicator is true if the respondent has a `"have now"` response for any of the variables `Q67AI` through `Q67AO`. This approach ensures that the calculation is comprehensive for each year.
#
# To ensure the shares are representative of the national population, the script produces weighted graphs and cross tabulations. We use the appropriate weights variable for each year's dataframe to calculate the average share. The 2005 data did not have weights available so it was omitted. 
#
# Null checks were performed for each year to ensure data quality before generating the indicators. The year 2015 had many rows with null values and all of these rows were dropped before calculating the indicators.

# ### 2005
#
# Notes:
# - Multiple different versions of life cover asked about including from employer, from trade union, and from church. 
# - Decided to exclude these to make it more comparable to future years and if my calculations are correct, it would only make a one percentage point difference.

df05, metadata05 = load_finscope_data(2005)
df05['burial_society_ind'] = (df05.Q50AJ==3).astype(int)
df05['funeral_insurance_ind'] = (df05[['Q50AH','Q50AI','Q50AK']]==3).any(axis=1).astype(int)
df05['life_insurance_ind'] = (df05.Q50AQ==3).astype(int)

# Null checks
print("df05 nulls:")
print(df05[['Q50AJ', 'Q50AH', 'Q50AI', 'Q50AK', 'Q50AQ']].isnull().sum())

# Investigate the additional life cover questions.

((df05.Q50AQ!=3)&((df05[['Q50AX','Q50AY','Q50AZ']]==3).any(axis=1))).mean()

(df05[['Q50AQ','Q50AX','Q50AY','Q50AZ']]==3).any(axis=1).mean()

# ### 2006
#
# Notes:
# - Survey administered by Research Surveys, different company from 2007
# - Only time I have seen that life insurance and funeral insurance got asked as part of the same section. 

df06, metadata06 = load_finscope_data(2006)
df06['burial_society_ind'] = (df06.Q67AP==3).astype(int)
df06['funeral_insurance_ind'] = (df06[['Q67AI','Q67AJ','Q67AK','Q67AL','Q67AM','Q67AN','Q67AO']]==3).any(axis=1).astype(int)
df06['life_insurance_ind'] = (df06.Q67BC==3).astype(int)
df06['weights'] = df06.Q600

# Null checks
print("df06 nulls:")
print(df06[['Q67AP', 'Q67AI','Q67AJ','Q67AK','Q67AL','Q67AM','Q67AN','Q67AO', 'Q67BC']].isnull().sum())

metadata06.variable_value_labels['Q67AP']

# ### 2007
#
# Notes:
# - There is a whole section devoted to life insurance, but is just a grouping for many types of insurance. In later years, this is renamed as the insurance section. 
# - The burial soceity option in the funeral insurance section is first rather than last. It also doesn't specificy "not AVBOB". 
#

df07, metadata07 = load_finscope_data(2007)
df07['burial_society_ind'] = (df07.Q128_A==3).astype(int)
df07['funeral_insurance_ind'] = (df07.filter(like='Q128_').drop(columns='Q128_A')==3).any(axis=1).astype(int)
df07['life_insurance_ind'] = (df07.Q145_A==3).astype(int)
df07['weights'] = df07.Q5006_

# Null checks
print("df07 nulls:")
print(df07[list(df07.filter(like='Q128_').columns) + ['Q145_A']].isnull().sum())

# ### 2008
#
# Notes:
# - In both 2008 and 2009, there are options to indicate if the respondent doesn't know what the product is. 

df08, metadata08 = load_finscope_data(2008)
df08['burial_society_ind'] = (df08.Q170_M==3).astype(int)
df08['funeral_insurance_ind'] = (df08.filter(like='Q170_').drop(columns='Q170_M')==3).any(axis=1).astype(int)
df08['life_insurance_ind'] = (df08.Q149_M==3).astype(int)
df08['weights'] = df08.Q5501_

# Null checks
print("df08 nulls:")
print(df08[list(df08.filter(like='Q170_').columns) + ['Q149_M']].isnull().sum())

# ### 2009
#
# Notes: 
# - There is a also a question as the beginning of the funeral insurance section that I havent' seen in other questionnaires that asks directly about funeral and life insurance.  Asks whether covered by funeral policy or burial soceity and whether pay themselves or covered by someone else. These types of questions got included in the main table breakdown of products in later years.

df09, metadata09 = load_finscope_data(2009)
df09['burial_society_ind'] = (df09.Q182_I==3).astype(int)
df09['funeral_insurance_ind'] = (df09.filter(like='Q182_').drop(columns='Q182_I')==3).any(axis=1).astype(int)
df09['life_insurance_ind'] = (df09.Q151_M==3).astype(int)
df09['weights'] = df09.Q9003_

# Null checks
print("df09 nulls:")
print(df09[list(df09.filter(like='Q182_').columns) + ['Q151_M']].isnull().sum())

metadata09.variable_value_labels['Q182_I']

metadata09.variable_value_labels['Q151_M']

# ### 2010
#
# Notes: 
# - Big difference from other 2015 and 2019 is the life insurance question Q151_M doesn't ask if covered by someone else. The options are:
#     - 1: ' Never had'
#     - 2: ' Used to have in the past but don’t have now'
#     - 3: ' Have now'
#     - 4: ' Dont know'
#     - 5: ' Not applicable'
# - And then the funeral insurance question is:
#     - 1: 'Never had and need'
#     - 2: 'Never had and don’t need'
#     - 3: 'Used to have in the past but dont have now'
#     - 4: 'Have now'
#     - 5: 'Dont know'

df10, metadata10 = load_finscope_data(2010)
df10['burial_society_ind'] = (df10.Q182_I==4).astype(int)
df10['funeral_insurance_ind'] = (df10.filter(like='Q182_').drop(columns='Q182_I')==4).any(axis=1).astype(int)
df10['life_insurance_ind'] = (df10.Q151_M==3).astype(int)
df10['weights'] = df10.Q9004_

# Null checks
print("df10 nulls:")
print(df10[list(df10.filter(like='Q182_').columns) + ['Q151_M']].isnull().sum())

# ### 2011
#
# Notes:
# - Survey provider is Ask Africa 

df11, metadata11 = load_finscope_data(2011)
df11['burial_society_ind'] = (df11.Q56_9==2).astype(int)
df11['funeral_insurance_ind'] = (df11.filter(like='Q56_').drop(columns='Q56_9')==2).any(axis=1).astype(int)
df11['life_insurance_ind'] = (df11.Q45_13==2).astype(int)
df11['weights'] = df11.WEIGHT

# Null checks
print("df11 nulls:")
print(df11[list(df11.filter(like='Q56_').columns) + ['Q45_13']].isnull().sum())

# ### 2012
#
# Notes:
# - Survey provider changes to TNS 

df12, metadata12 = load_finscope_data(2012)
df12['burial_society_ind'] = (df12.Q216_I==3).astype(int)
df12['funeral_insurance_ind'] = (df12.filter(like='Q216_').drop(columns='Q216_I')==3).any(axis=1).astype(int)
df12['life_insurance_ind'] = (df12.Q207_L==3).astype(int)
df12['weights'] = df12.Q5000_

# Null checks
print("df12 nulls:")
print(df12[list(df12.filter(like='Q216_').columns) + ['Q207_L']].isnull().sum())

# ### 2013

df13, metadata13 = load_finscope_data(2013)
df13['burial_society_ind'] = (df13.Q216_I==3).astype(int)
df13['funeral_insurance_ind'] = (df13.filter(like='Q216_').drop(columns='Q216_I')==3).any(axis=1).astype(int)
df13['life_insurance_ind'] = (df13.Q207_L==3).astype(int)
df13['weights'] = df13.Q5002_

# Null checks
print("df13 nulls:")
print(df13[list(df13.filter(like='Q216_').columns) + ['Q207_L']].isnull().sum())

# ### 2014

df14, metadata14 = load_finscope_data(2014)
df14['burial_society_ind'] = (df14.Q216_I==3).astype(int)
df14['funeral_insurance_ind'] = (df14.filter(like='Q216_').drop(columns='Q216_I')==3).any(axis=1).astype(int)
df14['life_insurance_ind'] = (df14.Q207_L==3).astype(int)
df14['weights'] = df14.Q5002_

# Null checks
print("df14 nulls:")
print(df14[list(df14.filter(like='Q216_').columns) + ['Q207_L']].isnull().sum())

# ### 2015

df15, metadata15 = load_finscope_data(2015)

# Null checks
print("df15 nulls:")
print(df15[['I1_09'] + list(df15.filter(like='I1_').drop(columns='I1_09').columns) + ['H1_12']].isnull().sum())

cols = ['I1_09', 'H1_12', 'Q5002_']
df15 = df15.dropna(subset=cols, how='all')

df15['burial_society_ind'] = (df15.I1_09==3).astype(int)
df15['funeral_insurance_ind'] = (df15.filter(like='I1_').drop(columns='I1_09')==3).any(axis=1).astype(int)
df15['life_insurance_ind'] = (df15.H1_12==3).astype(int)
df15['weights'] = df15.Q5002_

# ### 2016
#
# Notes:
# - Noticed that the i1_ burial society question specifically cross checks against the earlier Q.A8

df16, metadata16 = load_finscope_data(2016)
df16['burial_society_ind'] = (df16.I1_09==3).astype(int)
df16['funeral_insurance_ind'] = (df16.filter(like='I1_').drop(columns='I1_09')==3).any(axis=1).astype(int)
df16['life_insurance_ind'] = (df16.H1_12==3).astype(int)
df16['weights'] = df16.PP_BENCHWEIGHTx

# Null checks
print("df16 nulls:")
print(df16[['I1_09'] + list(df16.filter(like='I1_').drop(columns='I1_09').columns) + ['H1_12']].isnull().sum())

# ### 2017

df17, metadata17 = load_finscope_data(2017)
df17['burial_society_ind'] = (df17.I1_9==3).astype(int)
df17['funeral_insurance_ind'] = (df17.filter(like='I1_').drop(columns='I1_9')==3).any(axis=1).astype(int)
df17['life_insurance_ind'] = (df17.H1_12==3).astype(int)
df17['weights'] = df17.PP_BENCHWEIGHTx

# Null checks
print("df17 nulls:")
print(df17[['I1_9'] + list(df17.filter(like='I1_').drop(columns='I1_9').columns) + ['H1_12']].isnull().sum())

# ### 2018

df18, metadata18 = load_finscope_data(2018)
df18['burial_society_ind'] = (df18.I1_9==3).astype(int)
df18['funeral_insurance_ind'] = (df18.filter(like='I1_').drop(columns='I1_9')==3).any(axis=1).astype(int)
df18['life_insurance_ind'] = (df18.H1a_12==3).astype(int)
df18['weights'] = df18.BENCHWGT_PP

# Null checks
print("df18 nulls:")
print(df18[['I1_9'] + list(df18.filter(like='I1_').drop(columns='I1_9').columns) + ['H1a_12']].isnull().sum())

# ### 2019
#
# Notes:
# - For burial societies, we could use C7_3 or i1_10. The difference is C7_3 is only about their personal capacity and i1_10 asks as a type of funeral insurance. A quick check is that the mean of i1_10 is larger than C7_3.
# - All the i1_ questions have the following options:
#     - 1: 'Never had'
#     - 2: 'Used to have'
#     - 3: 'Have it in my name'
#     - 4: 'Covered by somebody else'
#     - 99: "Don't Know"

df19, metadata19 = load_finscope_data(2019)

# Burial Society indicator
df19['burial_society_ind'] = (df19.i1_10 == 3).astype(int)
# Funeral Insurance indicator (any i1_ column except i1_10 == 3)
df19['funeral_insurance_ind'] = (df19.filter(like='i1_').drop(columns='i1_10') == 3).any(axis=1).astype(int)
# Life Insurance indicator
df19['life_insurance_ind'] = (df19.H3a_13 == 3).astype(int)
df19['weights'] = df19.BENCHWGT_PP

# Null checks
print("df19 nulls:")
print(df19[['i1_10'] + list(df19.filter(like='i1_').drop(columns='i1_10').columns) + ['H3a_13']].isnull().sum())


# ## Figure

fig_data = []
fig_data_weighted = []

for y in range(6, 20):  # For years 2006 to 2019
    df_name = f"df{y:02d}"
    df = globals().get(df_name)
    if df is not None:
        fig_data.append({
            'year': y + 2000, 
            'burial_society': df.burial_society_ind.mean(),
            'funeral_insurance': df.funeral_insurance_ind.mean(),
            'life_insurance': df.life_insurance_ind.mean()
        })
        
        fig_data_weighted.append({
            'year': y + 2000, 
            'burial_society': np.average(df.burial_society_ind, weights=df.weights),
            'funeral_insurance': np.average(df.funeral_insurance_ind, weights=df.weights),
            'life_insurance': np.average(df.life_insurance_ind, weights=df.weights)
        })


df = pd.DataFrame(fig_data)
# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['year'], df['burial_society'], label='Burial Society', marker='o')
plt.plot(df['year'], df['funeral_insurance'], label='Funeral Insurance', marker='o')
plt.plot(df['year'], df['life_insurance'], label='Life Insurance', marker='o')
# Adding labels, title, and legend
plt.xlabel('Year')
plt.ylabel('Share')
plt.title('Shares of Burial Society, Funeral Insurance, and Life Insurance Over Time')
plt.legend()
plt.grid(True)
# Set y-axis limits
plt.ylim(0, .6)
# Add note about weighting
plt.figtext(0.5, -0.05, "Note: Survey weights have not been applied.", ha="center", fontsize=10)
# Show the plot
plt.show()

dfw = pd.DataFrame(fig_data_weighted)
# Plotting
plt.figure(figsize=(10, 6))
plt.plot(dfw['year'], dfw['burial_society'], label='Burial Society', marker='o')
plt.plot(dfw['year'], dfw['funeral_insurance'], label='Funeral Insurance', marker='o')
plt.plot(dfw['year'], dfw['life_insurance'], label='Life Insurance', marker='o')
# Adding labels, title, and legend
plt.xlabel('Year')
plt.ylabel('Share')
plt.title('Shares of Burial Society, Funeral Insurance, and Life Insurance Over Time')
plt.legend()
plt.grid(True)
# Set y-axis limits
plt.ylim(0, .6)
# Add note about weighting
plt.figtext(0.5, -0.05, "Note: Shares are weighted to be representative of the national population.", ha="center", fontsize=10)
# Show the plot
plt.show()

# ### Cross-tab

for y in range(6, 20):  # For years 2005 to 2019
    df_name = f"df{y:02d}"
    df = globals().get(df_name)
    if df is not None:
        print("Year: ", y + 2000)
        print(pd.crosstab(
            df.funeral_insurance_ind, 
            df.life_insurance_ind,  
            normalize='all', values=df.weights, aggfunc='sum',
            rownames=['Funeral Insurance'],
            colnames=['Life Insurance']))


for y in range(6, 20):  # For years 2005 to 2019
    df_name = f"df{y:02d}"
    df = globals().get(df_name)
    if df is not None:
        print("Year: ", y + 2000)
        print(pd.crosstab(
            df.burial_society_ind, 
            df.life_insurance_ind,  
            normalize='all', values=df.weights, aggfunc='sum',
            rownames=['Burial Society'],
            colnames=['Life Insurance']))

for y in range(6, 20):  # For years 2005 to 2019
    df_name = f"df{y:02d}"
    df = globals().get(df_name)
    if df is not None:
        print("Year: ", y + 2000)
        print(pd.crosstab(
            df.funeral_insurance_ind, 
            df.burial_society_ind,  
            normalize='all', values=df.weights, aggfunc='sum',
            rownames=['Funeral Insurance'],
            colnames=['Burial Society']))

