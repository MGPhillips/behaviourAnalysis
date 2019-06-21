def plot_speed_heatmap(df_rows):
    # fig, ax = plt.subplots(2,1)

    longest_flight_len = 0
    cmap = plt.cm.seismic  # coolwarm   #hot
    rankedData = pd.Series([])
    max_flight_len = 30 * 15
    max_speed = 0
    speed_limit = 10

    fig = plt.figure(figsize=(30, 30))
    ax0 = plt.subplot2grid((30, 30), (0, 0), colspan=19, rowspan=10)
    ax1 = plt.subplot2grid((30, 30), (0, 19), colspan=1, rowspan=10)

    for i in df_rows.index:

        if len(df_rows['distance_per_frame'][i]) == 0:
            continue

        if len(df_rows['distance_per_frame'][i]) > longest_flight_len:
            longest_flight_len = len(df_rows['distance_per_frame'][i][300 - 90:])

        if df_rows['distance_per_frame'][i].max() > max_speed:
            max_speed = df_rows['distance_per_frame'][i].max()

    if longest_flight_len > max_flight_len:
        longest_flight_len = max_flight_len

    for i in df_rows.index:

        speed = df_rows['distance_per_frame'][i][300 - 90:]

        speed[speed > speed_limit] = speed_limit

        pad_width = longest_flight_len - len(speed)

        if pad_width < 0:
            pad_width = 0

        speed = np.pad(speed, (0, pad_width), 'constant', constant_values=(0, 0))

        if len(speed) == 0:
            print('Speed empty')
            continue

        speed = smooth_array(speed, 5)

        if len(speed) > longest_flight_len:
            speed = speed[0:longest_flight_len]

        if len(rankedData) == 0:
            rankedData = speed

        else:

            rankedData = np.vstack([rankedData, speed])

    ind = []
    max_pos = []

    for i, d in enumerate(rankedData):
        ind.append(i)
        max_pos.append(np.where(rankedData[i] == rankedData[i].max())[0][0])

    zipped = zip(ind, max_pos)
    zipped = sorted(zipped, key=lambda t: t[1])
    index = [i[0] for i in zipped]
    rankedData = rankedData[index]

    rankedData = [x for x in rankedData if np.any(x)]

    vmax, vmin = speed_limit, -0
    # try:

    # print(rankedData)

    ax0.matshow(rankedData, cmap=cmap, vmin=vmin, vmax=vmax, interpolation='none', aspect='auto')
    norm = mpl.colors.Normalize(vmin=0, vmax=vmax)
    axymin, axymax = ax0.get_ylim()
    ax0.vlines([90], axymin, axymax, linestyles='dotted', color='w', linewidth=5)

    # ax2.axis('off')
    ax0.linewidth = 50.0
    cbar = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, spacing='proportional')
    cbar.set_label('cm/s', rotation=0, labelpad=10, y=1, color='w')
    # cbar.set_ticklabels(['Low', 'Medium'])# horizontal colorbar
    mpl.rcParams.update({'xtick.color': 'black', 'font.size': 15})  # 'font.size': 5,

    # except:
    # print('Speed could not be plotted', df_rows.index)

    plt.show()
    print(max_speed)

    return rankedData

light_flights = flight_df.loc[(flight_df['expt_type'] == 'light') &
                              (flight_df['flight_success'] == 'successful')]
dark_flights = flight_df.loc[(flight_df['expt_type'] == 'dark') &
                             (flight_df['flight_success'] == 'successful')]

light_df = plot_speed_heatmap(light_flights)
dark_df = plot_speed_heatmap(dark_flights)

#plot_speed_heatmap(flight_df.loc[(flight_df['flight_success'] == 'successful')])
