# set order of prop_type counts for ordering violin plot from most counts => lease counts
prop_type_order = list(df.prop_type.value_counts().index)

# new violin plot
#create violin plot
sns.set_context("talk")
sns.set_style("white")
fig, ax = pyplot.subplots(figsize=(20,6))
violin = sns.violinplot(ax=ax, x='prop_type', y='source_eui_norm', order=prop_type_order, data = df, inner='quartile', palette='deep', scale = 'width')
violin.set_title('Source EUI Distribution by Property Type')
violin.set_xticklabels(violin.get_xticklabels(), rotation=45)
