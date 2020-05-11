# create correlation df
features = df9[['gfa','num_bldgs','occ','numfloors', 'popdty', 'HHsize','%com', '%res', '%office', '%retail', '%garage', '%strge',
       '%factry', 'units/sf', 'resunits/sf', 'lastreno', 'age', 'complaints/sf', 'viol/sf', 'marketval/sf',
       'assesval/sf', 'source_eui_norm', 'ct/sf']]
correlations = features.corr()

#filter for just correlations with source_eui_norm
corr_eui = correlations[['source_eui_norm']].sort_values(by='source_eui_norm', ascending=False)
corr_eui = corr_eui.drop(index=['source_eui_norm'])

#create bar plot
sns.set(style="dark")
sns.set_context("talk")
f, ax = pyplot.subplots(figsize=(6, 10))

# feature correlations
sns.barplot(x='source_eui_norm', y=corr_eui.index, data=corr_eui)
ax.set(xlim=(-.25, .25), ylim=(-1,22), xlabel = "Correlation")
ax.set_title('Figure 2. Feature Correlation with Source EUI')
sns.despine(left=True, bottom=True)

