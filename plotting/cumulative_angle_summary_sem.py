flight_df['flight_success'] = flight_df.apply(get_flight_success, args=(40 * 30,), axis=1)

recent_mice_df = flight_df

interpolated_cums_dark = []
interpolated_cums_light = []

normalised_interpolated_dark = []
normalised_interpolated_light = []

for ind in recent_mice_df.index:

    if recent_mice_df['flight_success'][ind] != 'successful':
        continue

    flight_start = 300
    try:
        flight_start += np.where(recent_mice_df[recent_mice_df['experiment_name'] == '190401_dwm_light_us_619_3'][
                                     'distance_per_frame']['276'][300:] > 1.5)[0][0]
    except:
        print('could not add flight speed')

    cumulative = np.cumsum(recent_mice_df['vec_angles'][ind][flight_start:])

    x_interpolate = np.linspace(0, len(cumulative) - 1, 1000)
    x_cum = np.arange(len(cumulative))

    f_int = interp1d(x_cum, cumulative)

    if np.isnan(f_int(x_interpolate)).any():
        print(recent_mice_df['experiment_name'][ind])
        print(cumulative)

    # fig, ax = plt.subplots(2,1)
    interpolated = f_int(x_interpolate)

    normalised_interpolated = interpolated / interpolated[-1]

    # max_len = 500
    if recent_mice_df['expt_type'][ind] == 'dark':
        interpolated_cums_dark.append(interpolated)
        normalised_interpolated_dark.append(normalised_interpolated)

    if recent_mice_df['expt_type'][ind] == 'light':
        interpolated_cums_light.append(interpolated)
        normalised_interpolated_light.append(normalised_interpolated)

    # x_interpolate_plot = x_interpolate * (max_len/len(cumulative))

    # ax[0].plot(x_cum, cumulative)
    # ax[1].plot(x_interpolate_plot, f_int(x_interpolate))

## WITH SEM
from scipy import stats
dark_cum_means = np.nanmean(np.array(interpolated_cums_dark), axis=0)
dark_cum_sem = stats.sem(np.array(interpolated_cums_dark), nan_policy='omit')

light_cum_means = np.nanmean(np.array(interpolated_cums_light), axis=0)
light_cum_sem = stats.sem(np.array(interpolated_cums_light), nan_policy='omit')

normalised_dark_cum_means = np.nanmean(np.array(normalised_interpolated_dark), axis=0)
normalised_dark_cum_sem = stats.sem(np.array(normalised_interpolated_dark), nan_policy='omit')

normalised_light_cum_means = np.nanmean(np.array(normalised_interpolated_light), axis=0)
normalised_light_cum_sem = stats.sem(np.array(normalised_interpolated_light), nan_policy='omit')

x_plot = np.linspace(0, 1000, 1000)

fig,ax = plt.subplots(2,1,figsize=(10,20))

ax[0].plot(x_plot, dark_cum_means,
           color='magenta', linewidth= 3.0, label='Dark')
ax[0].fill_between(x_plot, dark_cum_means+dark_cum_sem, dark_cum_means-dark_cum_sem,
                  color='magenta', alpha=0.3)

ax[0].plot(x_plot, light_cum_means,
          color='blue', linewidth= 3.0, label='Light')
ax[0].fill_between(x_plot, light_cum_means+light_cum_sem, light_cum_means-light_cum_sem,
                  color='blue', alpha=0.3)



ax[1].plot(x_plot, normalised_dark_cum_means,
           color='magenta', linewidth= 3.0, label='Dark')
ax[1].fill_between(x_plot, normalised_dark_cum_means+normalised_dark_cum_sem,
                   normalised_dark_cum_means-normalised_dark_cum_sem,
                  color='magenta', alpha=0.3)

ax[1].plot(x_plot, normalised_light_cum_means,
          color='blue', linewidth= 3.0, label='Light')
ax[1].fill_between(x_plot, normalised_light_cum_means+normalised_light_cum_sem,
                   normalised_light_cum_means-normalised_light_cum_sem,
                  color='blue', alpha=0.3)

ax[1].set_title('Normalised cumulative trajectory angle change across flight')

x_line = np.linspace(0,1000, 1000)
y_line = np.linspace(0,1,1000)

ax[1].plot(x_line, y_line, color='gray', label='linear', linestyle=':')
ax[0].legend()
ax[1].legend()

