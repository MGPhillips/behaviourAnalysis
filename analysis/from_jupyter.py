



flight_df['rotation_angle']

for ind in flight_df.index:

    if abs(flight_df[flight_df.index == ind]['rotation_angle'].values[0]) < 5:
        continue

    fig, ax = plt.subplots(1, 4, figsize=(20, 5))

    x = flight_df[flight_df.index == ind]['x'].values[0][299:]

    mouse_colors = cm.Blues(np.linspace(0.5, 1, len(x)))
    shelter_colors = cm.Reds(np.linspace(0.5, 1, len(x)))
    rotation_colors = cm.Greens(np.linspace(0.5, 1, len(x)))

    ax[0].scatter(flight_df[flight_df.index == ind]['x'].values[0][299:],
                  flight_df[flight_df.index == ind]['y'].values[0][299:],
                  c=mouse_colors,
                  alpha=0.5, s=8)

    ax[0].scatter(flight_df[flight_df.index == ind]['rotation_x'].values[0][0::5],
                  flight_df[flight_df.index == ind]['rotation_y'].values[0][0::5],
                  color=shelter_colors, alpha=0.5, s=8)

    ax[0].scatter(flight_df[flight_df.index == ind]['shelter_x'].values[0][0::5],
                  flight_df[flight_df.index == ind]['shelter_y'].values[0][0::5],
                  color=rotation_colors, alpha=0.5, s=8)

    ax[0].set_ylim(0, 450)
    ax[0].set_xlim(0, 450)

    ang_err = flight_df[flight_df.index == ind]['start_traj_shelter_vector_angle'].values[0][299:]

    ax[1].hlines([flight_df[flight_df.index == ind]['rotation_angle']], 0, len(x))

    ax[1].plot(ang_err)

    normaliser = np.linspace(1, len(ang_err), len(ang_err))  #### This doesn't make sense
    cumsum = np.cumsum(ang_err) / normaliser

    ax[2].plot(cumsum)

    ax[3].plot(np.diff(ang_err))

    for i, title in enumerate(['Tracking', 'Angle Error',
                               'Cumulative angle sum normalised by time',
                               'Change in angle error']):
        ax[i].set_title(title)

    plt.show()

    exp_name = flight_df[flight_df.index == ind]['experiment_name'].values[0]
    subvid = flight_df[flight_df.index == ind]['subvid'].values[0]
    trial = flight_df[flight_df.index == ind]['stimulus_index'].values[0]

    print(exp_name)

    filename = exp_name + subvid + str(trial)

    print(filename)

    plt.savefig('E:\\Dropbox (UCL - SWC)\\big_Arena\\analysis\\paper_analysis\\rotation_errors\\' + filename)


def get_shelter_rotation_angle(row):
    centre = row['rotation_circle'][0], row['rotation_circle'][1]
    p1 = row['shelter_x'][0], row['shelter_y'][0]
    p2 = row['shelter_x'][-1], row['shelter_y'][-1]

    v1 = (centre[0] - p1[0], centre[1] - p1[1])
    v2 = (centre[0] - p2[0], centre[1] - p2[1])

    angle = angle_between_2(v1, v2)

    if angle > 180:
        angle = 360. - angle
        angle = -angle

    return angle


def get_rotation_angle(row):
    centre = row['rotation_circle'][0], row['rotation_circle'][1]
    p1 = row['rotation_x'][0], row['rotation_y'][0]
    p2 = row['rotation_x'][-1], row['rotation_y'][-1]

    v1 = (centre[0] - p1[0], centre[1] - p1[1])
    v2 = (centre[0] - p2[0], centre[1] - p2[1])  # v2 = (p2[0] - centre[0], p2[1] - centre[1])

    angle = angle_between_2(v1, v2)
    # a2 = angle_between(centre, p2)

    # angle = a1 - a2

    # print(row['rotation_x'][0])

    # v1 = [row['rotation_x'][0] - row['rotation_circle'][0], row['rotation_y'][0] - row['rotation_circle'][1]]
    # v2 = [row['rotation_x'][-1] - row['rotation_circle'][0], row['rotation_y'][-1] - row['rotation_circle'][1]]

    # angle = angle_between(v1, v2)
    # angle = np.degrees(angle)

    if angle > 180:
        angle = 360. - angle
        angle = -angle

    return angle


def get_speed(row):
    traj_x, traj_y = row['x'], row['y']
    dx, dy = (traj_x[1:] - traj_x[:-1], traj_y[1:] - traj_y[:-1])
    distance_travelled = np.sqrt(dx ** 2 + dy ** 2)

    return distance_travelled


def get_rolling_mean(arr, wind):
    df = pd.DataFrame({'A': arr})
    rolling_mean = df.rolling(wind).mean()  # .values[0]
    rolling_mean = np.reshape(rolling_mean['A'].values.tolist(), (len(rolling_mean), 1,)).T[0]

    # rolling_mean = rolling_mean.to_numpy() #list()
    return rolling_mean


def get_flight_response(row, data_df):
    name = row['experiment_name']

    name += row['subvid']

    ### Find all in nest indices
    # Compute accels and speeds first to avoid jumps between in nest periods
    # fig, ax = plt.subplots()
    x, y = data_df[data_df.index == name]['x'].values[0], data_df[data_df.index == name]['y'].values[0]
    # ax.scatter(x,y)

    print(x[0:100], y[0:100])
    x, y = get_rolling_mean(x, 5), get_rolling_mean(y, 5)
    # print(x[0:100], y[0:100])

    # ax.plot(x,y)
    # plt.show()
    dx, dy = (x[1:] - x[:-1], y[1:] - y[:-1])
    speed = data_df[data_df.index == name]['distance_per_frame'].values[0]
    accelerations = np.diff(speed)

    shelter = row['shelter_position']

    sdx, sdy = (x - row['shelter_position'][0], y - row['shelter_position'][1])

    shelter_distance_exploration = np.sqrt(sdx ** 2 + sdy ** 2)

    in_nest = np.where(shelter_distance_exploration < 30)[0]

    ### Delete in nest indices

    x_exp, y_exp = np.delete(x, in_nest), np.delete(y, in_nest)
    speeds_exp = np.delete(data_df[data_df.index == name]['distance_per_frame'].values[0], in_nest)  # .values[0]
    acceleration_exp = np.delete(accelerations, in_nest)

    ### Get baseline speed before flight and bin it

    speed_bins = np.linspace(0, 5, 16)  # 0,5,16

    speeds_exp_dig = np.digitize(speeds_exp, speed_bins)

    baseline_speed = np.mean(row['distance_per_frame'][269:299])

    baseline_bin = np.digitize(baseline_speed, speed_bins)

    speed_inds = np.where(speeds_exp_dig == baseline_bin)[0]

    speed_inds = speed_inds[speed_inds < len(x_exp) - 3000]

    if len(speed_inds) < 500:
        print('Speed inds too short -- returning nan')
        return (np.nan)

    ### Get inidices in the same bin as the baseline speed
    random_speed_inds = np.random.choice(speed_inds, 500)

    ### Take random sample of post baseline speeds from exploration
    speeds = [speeds_exp[x:x + 270].tolist() for x in random_speed_inds]

    speeds_array = np.array([np.array(xi) for xi in speeds])
    peak_speeds = [np.amax(x) for x in speeds]

    ### Use random sample to compute 95 percentile
    threshold = np.percentile(speeds_array, 95, axis=0)

    ### Test where flight goes above 95 percentile

    rt = np.where(row['distance_per_frame'][299:299 + 270] > threshold)[0]

    if len(rt) == 0:
        rt = [np.nan]

    if len(rt) != 0:
        rt = rt[0]

    return rt


data_df['distance_per_frame'] = data_df.apply(get_speed, axis=1)
flight_df['reaction_classification'] = flight_df.apply(get_flight_response, args=(data_df,), axis=1)