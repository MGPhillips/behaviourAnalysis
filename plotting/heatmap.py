def plot_heatmap(data_df_rows, flight_df_rows, exp_name):
    plt.close('all')

    session_x, session_y = np.array([]), np.array([])

    for i, d in enumerate(data_df_rows):
        session_x = np.concatenate((session_x, data_df_rows[i]['x'][0]))
        session_y = np.concatenate((session_y, data_df_rows[i]['y'][0]))

    data = np.vstack([list(session_x), list(session_y)]).T

    x, y = data.T

    ##################################################################
    # HEATMAP + FLIGHTS  # NORMALISED FLIGHTS # FLIGHT SPEED HEATMAP #
    ##################################################################

    nbins = 100
    # fig, axes = plt.subplots(figsize=(26, 20))

    fig = plt.figure(figsize=(30, 30))
    ax0 = plt.subplot2grid((30, 30), (0, 0), colspan=14, rowspan=14)
    ax1 = plt.subplot2grid((30, 30), (0, 15), colspan=15, rowspan=15)
    ax2 = plt.subplot2grid((30, 30), (20, 0), colspan=19, rowspan=10)
    ax3 = plt.subplot2grid((30, 30), (20, 19), colspan=1, rowspan=10)
    ax4 = plt.subplot2grid((30, 30), (20, 20), colspan=10, rowspan=10)

    k = kde.gaussian_kde(data.T)

    xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]

    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    ax0.set_title('Heatmap of exploration with trajectories overlaid')
    pcm = ax0.pcolormesh(xi, yi, zi.reshape(xi.shape), norm=colors.LogNorm(vmin=zi.min(), vmax=zi.max()),
                         shading='gouraud', cmap=plt.cm.gist_gray)  # cmap=plt.cm.PuBu_r

    fig.colorbar(pcm, ax=ax0, extend='max')

    for i, d in enumerate(flight_df_rows.index):

        ax0.scatter(flight_df_rows['x'][i], flight_df_rows['y'][i], s=20, alpha=0.5)  # color='magenta',

        try:
            ax1.scatter(flight_df_rows['conv_xy'][i][0], flight_df_rows['conv_xy'][i][1], s=10, alpha=0.5)

        except:
            print('conv_xy = nan')

    ax1.set_xlim([-500, 500])
    ax1.set_ylim([0, 600])

    cmap = plt.cm.hot

    rankedData = pd.Series([])
    max_flight_len = 30 * 12
    longest_flight_len = 0
    max_speed = 0
    speed_limit = 15

    ###### PUT A LIMIT ON MAX SPEED

    for i in flight_df_rows.index:

        if len(flight_df_rows['distance_per_frame'][i]) == 0:
            continue

        if len(flight_df_rows['distance_per_frame'][i]) > longest_flight_len:
            longest_flight_len = len(flight_df_rows['distance_per_frame'][i][300 - 90:])

        if flight_df_rows['distance_per_frame'][i].max() > max_speed:
            max_speed = flight_df_rows['distance_per_frame'][i].max()

    if longest_flight_len > max_flight_len:
        longest_flight_len = max_flight_len

    for i in flight_df_rows.index:

        speed = flight_df_rows['distance_per_frame'][i][300 - 90:]

        speed[speed > speed_limit] = speed_limit

        pad_width = longest_flight_len - len(speed)

        if pad_width < 0:
            pad_width = 0

        # print('Speed:', speed)
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

    vmax, vmin = speed_limit, -0
    try:
        ax2.matshow(rankedData, cmap=cmap, vmin=vmin, vmax=vmax, interpolation='none', aspect='auto')
        norm = mpl.colors.Normalize(vmin=0, vmax=vmax)
        ax2ymin, ax2ymax = ax2.get_ylim()
        ax2.vlines([90], ax2ymin, ax2ymax, linestyles='dotted', color='w', linewidth=5)

        # ax2.axis('off')
        ax2.linewidth = 50.0
        cbar = mpl.colorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, spacing='proportional')
        cbar.set_label('cm/s', rotation=0, labelpad=10, y=1, color='w')
        # cbar.set_ticklabels(['Low', 'Medium'])# horizontal colorbar
        mpl.rcParams.update({'xtick.color': 'black', 'font.size': 15})  # 'font.size': 5,

    except:
        print('Speed could not be plotted', flight_df_rows.index)

    for i in flight_df_rows.index:
        try:
            start_distance = flight_df_rows['shelter_distance'][i][300]
            distance_in_flight = sum(flight_df_rows['distance_per_frame'][i][300:])

            ax4.scatter(start_distance, distance_in_flight, c='navy')
        except:
            print('Ind out of range')

    ax4.set_ylim(ymin=0)
    ax4.set_xlim(xmin=0)
    ax4.set_title('Flight Accuracy Overview')
    ax4.set_ylabel('Distance travelled in flight')
    ax4.set_xlabel('Start distance to nest')

    plt.tight_layout()

    figname = 'E:\\big_arena_analysis\\session_summary_{}'.format(exp_name)
    fig.savefig(figname, dpi=fig.dpi)


completed_indices = []

for index in data_df.index:

    if index[0:-1] in completed_indices:
        continue

    print(index[0:-1])

    completed_indices.append(index[0:-1])

    indices = [x for x in data_df.index if index[0:-1] in x]
    data_df_rows = []

    for i in indices:
        data_df_rows.append(data_df[data_df.index == i])

    plot_heatmap(data_df_rows, flight_df[flight_df['experiment_name'] == index[0:-1]], index[0:-1])
