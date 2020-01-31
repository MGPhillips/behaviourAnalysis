########## MAX SPEEDS




ax = sns.distplot(flight_df[flight_df['flight_success']=='successful'][
    flight_df['expt_type']=='dark']['max_speed']/10, color=colors['dark'], label='dark') #, kde=False#shade=True,
ax = sns.distplot(flight_df[flight_df['flight_success']=='successful'][
    flight_df['expt_type']=='light']['max_speed']/10, color=colors['light'], label='light') #kde=False #shade=True,


ax.set(xlabel='Max speed (m/s)', ylabel='Density')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_title('Distribution of maximum speeds in successful flights')



############### MEAN SPEEDS


ax = sns.distplot(flight_df[flight_df['flight_success']=='successful'][
    flight_df['expt_type']=='dark']['mean_speed']/10, color=colors['dark'], label='dark')

ax = sns.distplot(flight_df[flight_df['flight_success']=='successful'][
    flight_df['expt_type']=='light']['mean_speed']/10, color=colors['light'], label='light')


ax.set(xlabel='Mean speed (m/s)', ylabel='Density')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_title('Distribution of mean speeds in successful flights')