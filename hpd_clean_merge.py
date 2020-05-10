#find year of complaint
hpd_complaints['yr_entered'] = hpd_complaints['ReceivedDate'].str[-4:].astype(int)

#filter dataset for years after 1999 and before 2021
hpd_complaints = hpd_complaints.loc[ (hpd_complaints['yr_entered'] > 1999) & (hpd_complaints['yr_entered'] < 2021), : ]

#create bbls
hpd_complaints['bbl'] = hpd_complaints['BoroughID'].astype(str) + hpd_complaints['Block'].astype(str).str.zfill(5) \
                        + hpd_complaints['Lot'].astype(str).str.zfill(4)

#groupby bbl
hpd_complaints_counts = hpd_complaints.groupby(['bbl']).count()

#drop all columns except 1
hpd_complaints_counts = hpd_complaints_counts.drop(columns = ['BuildingID', 'BoroughID', 'Borough', 'HouseNumber',
       'StreetName', 'Zip', 'Block', 'Lot', 'Apartment', 'CommunityBoard',
       'ReceivedDate', 'StatusID', 'Status', 'StatusDate', 'yr_entered'])

# create bbl_ columns for merging, convert to int for merging
hpd_complaints_counts['bbl_'] = hpd_complaints_counts.index
hpd_complaints_counts['bbl_'] = pd.to_numeric(hpd_complaints_counts.bbl_, errors='coerce')
hpd_complaints_counts['bbl_'] = hpd_complaints_counts['bbl_'].dropna()
hpd_complaints_counts['bbl_'] = hpd_complaints_counts['bbl_'].astype(int, errors='ignore')

#drop duplicates
hpd_complaints_counts = hpd_complaints_counts.drop_duplicates(subset = 'bbl_')

#merge datasets
df5_merge = df5.merge(hpd_complaints_counts, how='left', left_on='bbl', right_on='bbl_')

#drop new redundant columns
df5_merge = df5_merge.drop(columns='bbl_')

#rename new columns
df5_merge = df5_merge.rename(columns={'ComplaintID': '20yrhpd_complaints'})

#fill NAs with zero to indicates buildings have not recieved any complaints
df5_merge['20yrhpd_complaints'] = df5_merge['20yrhpd_complaints'].fillna(0)
