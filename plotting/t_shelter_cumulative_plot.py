#import seaborn as sns
colors = {'dark': 'mediumvioletred',
              'light': 'royalblue'}

ax = sns.distplot(flight_df[(flight_df['expt_type']=='dark') & (flight_df['t_to_nest']<1000)]['t_to_nest']/30, color=colors['dark'], label='dark') #, kde=False#shade=True,
ax = sns.distplot(flight_df[(flight_df['expt_type']=='light') & (flight_df['t_to_nest']<1000)]['t_to_nest']/30, color=colors['light'], label='light') #kde=False #shade=True,


ax.set(xlabel='t to shelter', ylabel='Density')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_title('Distribution t to shelter')
#ax.set_xlim(0,1000)