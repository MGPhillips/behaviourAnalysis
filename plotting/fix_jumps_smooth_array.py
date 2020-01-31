def fix_jumps(y, distance_jump_limit):
    # Create array of distance travelled
    dist = np.zeros([len(y), 1])
    speed = np.zeros([len(y), 1])

    # Iterate through x
    for i in range(len(y)):
        if i < len(y) - 1:
            # Get distance between points
            dist[i] = (y[i + 1] - y[i])

            if dist[i] > distance_jump_limit:
                # print('dist = ', dist[i])
                y[i + 1] = y[i]

    return y


def smooth_array(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


for i in flight_df.index:
    ang = flight_df['head_shelter_angle'][i]  # [300:]
    # angles = fix_jumps(ang, 10)
    # angles = smooth_array(ang, 5)
    r = np.linspace(0, len(angles), len(angles))

    # angles = fix_tracking

    ax = plt.subplot(111, projection='polar')
    ax.plot(angles, r)
    # ax.set_rmax(2)
    ax.set_rticks([])  # less radial ticks
    # ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(False)
    ax.set_theta_zero_location("N")
    ax.set_title("A line plot on a polar axis", va='bottom')
    plt.show()