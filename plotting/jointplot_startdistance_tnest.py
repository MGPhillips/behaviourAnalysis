a = sns.jointplot('start_distance', 't_to_nest',
              data=recent_mice_df.loc[(recent_mice_df['flight_success'] == 'successful') &
                                      (recent_mice_df['expt_type'] == 'dark')],
              color='magenta',
              kind="reg") #

sns.jointplot('start_distance', 't_to_nest',
              data=recent_mice_df.loc[(recent_mice_df['flight_success'] == 'successful') &
                                      (recent_mice_df['expt_type'] == 'light')],
              color='blue',
              kind="reg") #