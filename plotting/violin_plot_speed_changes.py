fig, ax = plt.subplots()

##for ind in flight_df.index:
expt_type_pal = {'light': 'blue', 'dark': 'magenta'}
ax = sns.violinplot(x='expt_type', y='abs_speed_change_sum', data=recent_mice_df, palette=expt_type_pal)