# we see there are many outliers, let's trim the outliers
# first calculate the zscore for each fuel and each building within it's own property type
# append the zscore in a new respective column

df['zscore'] = 0
for prop_type in top10_prop_types:
    prop_filter = df.loc[ df['prop_type'] == prop_type, 'source_eui_norm']
    df.loc[ df['prop_type'] == prop_type, 'zscore' ] \
    = np.abs(stats.zscore(prop_filter))
    
df['zscore_elec'] = 0
for prop_type in top10_prop_types:
    prop_filter = df.loc[ df['prop_type'] == prop_type, 'elec_kbtu']
    df.loc[ df['prop_type'] == prop_type, 'zscore_elec' ] \
    = np.abs(stats.zscore(prop_filter))
    
df['zscore_ng'] = 0
for prop_type in top10_prop_types:
    prop_filter = df.loc[ df['prop_type'] == prop_type, 'ng']
    df.loc[ df['prop_type'] == prop_type, 'zscore_ng' ] \
    = np.abs(stats.zscore(prop_filter))
    
df['zscore_oil2'] = 0
for prop_type in top10_prop_types:
    prop_filter = df.loc[ df['prop_type'] == prop_type, 'oil2']
    df.loc[ df['prop_type'] == prop_type, 'zscore_oil2' ] \
    = np.abs(stats.zscore(prop_filter))
    
df['zscore_steam'] = 0
for prop_type in top10_prop_types:
    prop_filter = df.loc[ df['prop_type'] == prop_type, 'district_steam'].astype(float)
    df.loc[ df['prop_type'] == prop_type, 'zscore_steam' ] \
    = np.abs(stats.zscore(prop_filter))
    
df['zscore_oil6'] = 0
for prop_type in top10_prop_types:
    prop_filter = df.loc[ df['prop_type'] == prop_type, 'oil6']
    df.loc[ df['prop_type'] == prop_type, 'zscore_oil6' ] \
    = np.abs(stats.zscore(prop_filter))
    
df['zscore_oil4'] = 0
for prop_type in top10_prop_types:
    prop_filter = df.loc[ df['prop_type'] == prop_type, 'oil4']
    df.loc[ df['prop_type'] == prop_type, 'zscore_oil4' ] \
    = np.abs(stats.zscore(prop_filter))
    
#drop buildings where the zscore meets or exceeds the threshold
threshold = 3
df = df.loc[ df['zscore'] < threshold, : ]
df = df.loc[ df['zscore_ng'] < threshold, : ]
df = df.loc[ df['zscore_elec'] < threshold, : ]
df = df.loc[ df['zscore_steam'] < threshold, : ]
df = df.loc[ df['zscore_oil2'] < threshold, : ]
df = df.loc[ df['zscore_oil4'] < threshold, : ]
df = df.loc[ df['zscore_oil6'] < threshold, : ]

# replace any use type that occurs less than 50 times with 'Other'
df['use_1'][ df['use_1'].isin(df['use_1'].value_counts()[df['use_1'].value_counts() < 50].index)] = 'Other'
df['use_2'][ df['use_2'].isin(df['use_2'].value_counts()[df['use_2'].value_counts() < 50].index)] = 'Other'
df['use_3'][ df['use_3'].isin(df['use_3'].value_counts()[df['use_3'].value_counts() < 50].index)] = 'Other'
