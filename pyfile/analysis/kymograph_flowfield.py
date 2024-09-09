import numpy as np
import matplotlib.pyplot as plt


n = 2560
r_ratio = 1.3

path = 'data/volvox/20240906_volvox_symplectic_k=2.35/'

ur_data = np.load(f'{path}ur_data_fil{n}_r{r_ratio}.npy')
utheta_data = np.load(f'{path}utheta_data_fil{n}_r{r_ratio}.npy')
grid_shape = np.load(f'{path}grid_shape_fil{n}_r{r_ratio}.npy')


selected_t = 0
n_frame = ur_data.shape[0]
# n_frame = 120

ur_data = ur_data[:n_frame]
utheta_data = utheta_data[:n_frame]
n_r, n_phi, n_theta = grid_shape
# print(n_r, n_phi, n_theta)

# assuming n_r = 1
reshaped_ur_data = ur_data.reshape(n_frame, n_phi, n_theta)
reshaped_utheta_data = utheta_data.reshape(n_frame, n_phi, n_theta)

avg_over_time_ur_data = np.mean(reshaped_ur_data, axis=0)
avg_over_time_utheta_data = np.mean(reshaped_utheta_data, axis=0)

reshaped_ur_data -= avg_over_time_ur_data
reshaped_utheta_data -= avg_over_time_utheta_data

avg_ur_data = reshaped_ur_data.mean(axis=1)
avg_utheta_data = reshaped_utheta_data.mean(axis=1)



avg_ur_data = np.tile(avg_ur_data, (10,1))
avg_utheta_data = np.tile(avg_utheta_data, (10,1))



# print(avg_ur_data)
# print(avg_utheta_data)

t = n_frame/30

fig1 = plt.figure(figsize=(8,2))
ax1 = fig1.add_subplot()
fig2 = plt.figure(figsize=(8,2))
ax2 = fig2.add_subplot()
fig3 = plt.figure()
ax3 = fig3.add_subplot()


# phi_var_plot = ax3.imshow(reshaped_ur_data[selected_t].T, cmap='jet', origin='upper', extent=[0, 2*np.pi, 0, np.pi])
phi_var_plot = ax3.imshow(avg_over_time_ur_data.T, cmap='jet', origin='upper', extent=[0, 2*np.pi, 0, np.pi])
fig3.colorbar(phi_var_plot)

ur_plot = ax1.imshow(avg_ur_data.T, cmap='jet', origin='upper', extent=[0, t, 0, 2*np.pi], aspect='auto')
utheta_plot = ax2.imshow(avg_utheta_data.T, cmap='jet', origin='upper', extent=[0, t, 0, 2*np.pi], aspect='auto')

fig1.colorbar(ur_plot)
fig2.colorbar(utheta_plot)


y_ticks = np.linspace(0, 2*np.pi, 5)
y_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$' ][::-1]
y_labels = [r'$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$' ][::-1]
ax1.set_yticks(ticks=y_ticks, labels=y_labels)
ax2.set_yticks(ticks=y_ticks, labels=y_labels)

ax1.set_xlabel(r'$t/T$')
ax1.set_ylabel(r'$\theta$')

ax2.set_xlabel(r'$t/T$')
ax2.set_ylabel(r'$\theta$')

ax3.set_xlabel(r'$\phi$')
ax3.set_ylabel(r'$u_{\theta}$')
ax3.set_aspect('equal')
ax3_x_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$' ]
ax3_y_labels = [r'$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$' ][::-1]
ax3.set_xticks(ticks= np.linspace(0, 2*np.pi, 5), labels=ax3_x_labels)
ax3.set_yticks(ticks= np.linspace(0, np.pi, 5), labels=ax3_y_labels)
ax3.set_title(rf'$u_r$, $t={selected_t}$')

fig1.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
fig1.savefig(f'fig/ur_fil{n}_r{r_ratio}.pdf', bbox_inches = 'tight', format='pdf')
fig2.savefig(f'fig/utheta_fil{n}_r{r_ratio}.pdf', bbox_inches = 'tight', format='pdf')
# fig3.savefig(f'fig/ur_variation_over_phi_fil{n}_r{r_ratio}.pdf', bbox_inches = 'tight', format='pdf')

plt.show()