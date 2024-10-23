import matplotlib.pyplot as plt
import lightkurve as lk
import pandas as pd
import numpy as np

#-------------------------------------------------------------------input start---------------------------------------------------------------

obj = #STR name of the target ffrom TESS or Kepler catalogue 
sector = #STR TESS sector of observation
author = #STR Preparation pipeline used as data author

lc = lk.search_lightcurve(obj, sector=sector, author=author)[0].download()
time_beggening = int(input("t0")) # Chosen starting time for given lightcurve
time_end = int(input("tmax")) # Chosen endtime for given lightcurve
if time_end == 0:
    time_end = 999999999999
else:
    time_end = time_end 
#-----------------------------------------------------------------data frame body--------------------------------------------------------------
    
lc.to_csv("CSV/raw_data.csv", overwrite = True)
lc_data = pd.read_csv("CSV/lc_dataframe.csv")
raw_data = pd.read_csv("CSV/raw_data.csv")
    
lc_data = raw_data[(raw_data["time"] >= time_beggening) & (raw_data["time"] <= time_end)]
lc_data.to_csv("CSV/lc_dataframe.csv")
    
    
time_by_pg = lc_data["time"]/pg
lc_data["time by Pg"] = time_by_pg
    
    
    
P0 = lc_data["time by Pg"].min()
lc_data["delta P from P0"] = lc_data["time by Pg"] - P0
    
lc_data["nPeriod"] = lc_data["delta P from P0"].apply(np.floor)
    
lc_data.to_csv("CSV/lc_dataframe.csv")
#------------------------------------------------------------------datafilter----------------------------------------------------------------
    
df = pd.DataFrame(list())
df.to_csv('CSV/lc_filter.csv')
filter = pd.read_csv("CSV/lc_filter.csv")
    
    
filter["time"] = lc_data["time"]
filter.to_csv("CSV/lc_filter.csv") 
    
filter["flux"] = lc_data["flux"]
filter["time by Pg"] = lc_data["time by Pg"]
filter["nPeriod"] = lc_data["nPeriod"]
    
filter.to_csv("CSV/lc_filter.csv")
#--------------------------------------------------------------Period separator-------------------------------------------------------------
df = filter
unique_categories = df['nPeriod'].unique()
dataframes_by_category = {}
    
# -------------------------------------------------------------
for category in unique_categories:
    category_df = df[df['nPeriod'] == category]
    dataframes_by_category[category] = category_df
    
# -------------------------------------------------------------
for category, category_df in dataframes_by_category.items():
    file_name = f"CSV/Periods/Period {category}.csv"
    category_df.to_csv(file_name, index=False)
#----------------------------------------------------------------Period Finder-----------------------------------------------------------
    
n = int(filter["nPeriod"].max())
t_values = []
    
for period in range(n+1):
    file_path = f"CSV/Periods/Period {period}.0.csv"
    try:
        period_df = pd.read_csv(file_path)
        t_max = period_df['time'][period_df['flux'].idxmax()]
        t_values.append(t_max)
    except FileNotFoundError:
        print(f"Skipping missing data for Period {period}")
        continue
    
P_values = []
    
for i in range(1, len(t_values)):
    P_values.append(t_values[i] - t_values[i - 1])
    
valid_P_values = [P for P in P_values if not np.isnan(P)]
if valid_P_values:
    calculated_period = sum(valid_P_values) / len(valid_P_values)
else:
    calculated_period = np.nan
    
for P in enumerate(P_values, start=1):
    print(P[1])
    
print(f"period: {calculated_period}")
