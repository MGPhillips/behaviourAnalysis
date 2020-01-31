def plot_conv_xy(ax, df, color, n_traj):
    inds = random.sample(range(0, len(df)), n_traj)
    count = 0

    for i, ind in enumerate(inds):

        # df[df.index==ind]['conv_xy'][0][0], df[df.index==ind]['conv_xy'][0][1] / conversion_factor

        index = df.index[ind]

        conversion_factor = df[df.index == index]['start_distance'][0]
        # print('Conversion factor = ', conversion_factor)

        x, y = fix_tracking(df[df.index == index]['conv_xy'][0][0], df[df.index == index]['conv_xy'][0][1],
                            zeros_fun, 20)
        y = y / conversion_factor

        if any(j > 1.1 for j in y):
            continue

        ax.plot(x, y, c=color,
                alpha=0.7)

    ax.set_xlim(-250, 250)

    return ax


def plot_conv_xy_interpolated_distance_to_midline(ax, df, color):
    n_interps = 500
    interp = np.linspace(0, 1, n_interps)

    n_rows = len(df.index)

    xs, ys = np.zeros((n_rows, n_interps), dtype=float), np.zeros((n_rows, n_interps), dtype=float)

    for j, ind in enumerate(df.index):

        index = df[df.index == ind].index

        conversion_factor = df[df.index == ind]['start_distance'][index].values[0]

        x, y = df[df.index == ind]['conv_xy'].values[0][0], df[df.index == ind]['conv_xy'].values[0][1]
        # print('len:',len(x))

        i = np.linspace(0, 1, len(x))
        # _i = np.linspace(0,1,len(y))

        # x,y = fix_tracking(x,y,zeros_fun, 20)

        if len(x) == 0:
            continue

        x = abs(x)

        y = y / conversion_factor

        xinterp = np.interp(interp, i, x)
        yinterp = np.interp(interp, i, y)
        xs[j], ys[j] = xinterp, yinterp

        # yinterp = yinterp/500

    # print(x)
    # rint(xinterp)
    # ax.plot(xinterp,yinterp, c=color, alpha=0.7)
    ax.plot(np.mean(xs, axis=0), np.mean(ys, axis=0), c=color, alpha=1, linewidth=3)
    # ax.fill_betweenx(np.mean(ys, axis=0),
    #                np.mean(xs, axis=0)-np.std(xs, axis=0),
    #                np.mean(xs, axis=0)+np.std(xs, axis=0),
    #                color=color, alpha=0.4)

    return ax


fig, ax = plt.subplots(figsize=(2, 6))

ax = plot_conv_xy_interpolated_distance_to_midline(ax, flight_df[(flight_df['expt_type'] == 'dark') &
                                                                 (flight_df['flight_success'] == 'successful')],
                                                   colors['dark'])
ax = plot_conv_xy_interpolated_distance_to_midline(ax, flight_df[(flight_df['expt_type'] == 'light') &
                                                                 (flight_df['flight_success'] == 'successful')],
                                                   colors['light'])

# for axis in ax:
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# ax.spines['left'].set_bounds(0, 1)
# ax.set_ylim([0., 1.0])
ax.set_xlim([-10, None])

# ax[1].spines['left'].set_visible(False)
# ax[1].tick_params(labelleft=False)
# ax[1].tick_params(left=False)

ax.set_ylabel('Normalised distance to shelter')
ax.set_xlabel('Deviation from direct path')

# ax[0].set_title('Dark')
# ax[1].set_title('Light')


fig.suptitle('Normalised trajectories', fontsize=16)