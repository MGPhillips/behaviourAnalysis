fig, ax = plt.subplots()

for trial in flight_df.loc[(flight_df['expt_type'] == 'light') &
                           (flight_df['dwm_trial'] != True) &
                          (flight_df['flight_success']=='successful')].index:

    length_normalisation = flight_df['conv_xy'][trial][1].max() / 500

    ax.plot(flight_df['conv_xy'][trial][0], flight_df['conv_xy'][trial][1] / (length_normalisation * 500),
               alpha=0.5, color='navy') #s=1.0

#ax = plt.gca()
ax.axes.get_xaxis().set_ticks([])
ax.axes.get_xaxis().set_visible(False)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_linewidth(2)

ax.set_ylabel('Normalised distance', fontweight='bold')

ax.set_xlim(-200, 400)
ax.set_ylim(0, 1.1)

ax.tick_params(axis='both', which='major', labelsize=14, width=2)


plt.savefig('E:\\Dropbox (UCL - SWC)\\big_Arena\\analysis\\upgrade_figures\\test.png', dpi=1000)
plt.show()
#plt.savefig('E:\\Dropbox (UCL - SWC)\\big_Arena\\analysis\\upgrade_figures\\test.eps')