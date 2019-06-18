fig, axes = plt.subplots(2, 1, figsize=(7, 14))
flight_type = ['dark', 'light']
reds = plt.get_cmap("Reds")
# plt.scatter(x, y, c=x, s=100, cmap=reds)


for i, ax in enumerate(axes):
    for trial in flight_df.loc[(flight_df['expt_type'] == flight_type[i]) &
                               (flight_df['flight_success'] == 'successful')].index:
        len_trial = len(flight_df['conv_xy'][trial][0])
        length_normalisation = flight_df['conv_xy'][trial][1].max() / 500
        # print(length_normalisation)
        ax.scatter(flight_df['conv_xy'][trial][0], flight_df['conv_xy'][trial][1] / (length_normalisation * 500),
                   alpha=0.5, c=flight_df['distance_per_frame'][trial][300:300 + len_trial], cmap=reds,
                   s=1.0)

    ax.set_xlim(-500, 500)
    ax.set_ylim(0, 1.2)