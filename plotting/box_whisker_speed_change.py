ax = sns.boxplot(x='expt_type', y='abs_speed_change_sum', data=recent_mice_df)
ax = sns.stripplot(x='expt_type', y='abs_speed_change_sum', data=recent_mice_df, color="gray", jitter=0.2, size=2.5)