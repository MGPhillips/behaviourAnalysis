

fig,ax = plt.subplots()

l_means = np.mean(light_d, axis = 0)
d_means = np.mean(dark_d, axis = 0)
l_sem = np.std(light_d, axis=0)
d_sem = np.std(dark_d, axis=0)
x = np.arange(450)
ax.plot(x, l_means, c='blue')
ax.plot(x, d_means,c='magenta')

ax.fill_between(x, l_means-l_sem, l_means+l_sem, color='blue', alpha=0.1)
ax.fill_between(x, d_means-d_sem, d_means+d_sem, color='magenta', alpha=0.1)