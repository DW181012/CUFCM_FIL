
import numpy as np
import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
mpl.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
mpl.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'

plt.rcParams.update({'font.size': 18})

path_heldfixed = "data/ic_hpc_sim/"
path_free = "data/ic_hpc_sim_free/"

r_data_heldfixed = np.load(f"{path_heldfixed}r_data.npy")
k_data_heldfixed = np.load(f"{path_heldfixed}k_data.npy")

r_data_free = np.load(f"{path_free}r_data.npy")
k_data_free = np.load(f"{path_free}k_data.npy")
avg_speed_data_free = np.load(f"{path_free}avg_speed_data.npy")
avg_speed_along_axis_data_free = np.load(f"{path_free}avg_speed_along_axis_data.npy")
avg_rot_speed_along_axis_data_free = np.load(f"{path_free}avg_rot_speed_along_axis_data.npy")
avg_vz_data_free = np.load(f"{path_free}avg_vz_data.npy")
# eff_data_free = np.load(f"{path_free}eff_data.npy")

n_folder_heldfixed = r_data_heldfixed.shape[0]
n_folder_free = r_data_free.shape[0]

dpi = 100

fig = plt.figure(dpi=dpi)
ax = fig.add_subplot(1,1,1)
fig2 = plt.figure(dpi=dpi)
ax2 = fig2.add_subplot(1,1,1)
fig3 = plt.figure(dpi=dpi)
ax3 = fig3.add_subplot(1,1,1)
# fig4 = plt.figure(dpi=dpi)
# ax4 = fig4.add_subplot(1,1,1)
# fig5 = plt.figure(dpi=dpi)
# ax5 = fig5.add_subplot(1,1,1)

for fi in range(n_folder_heldfixed):
    plot_x = k_data_heldfixed[fi] 
    plot_y = r_data_heldfixed[fi]
    indices_symplectic = np.where(plot_y > .4)[0]
    indices_diaplectic = np.where((plot_y  < .4) & (plot_y > 0.04))[0]
    indices_diaplectic_k2 = np.where(plot_y  < 0.04)[0]

    ax.scatter(plot_x[indices_symplectic], plot_y[indices_symplectic], s=100, marker='+', c='r')
    ax.scatter(plot_x[indices_diaplectic], plot_y[indices_diaplectic], s=100, marker='+', c='r')
    ax.scatter(plot_x[indices_diaplectic_k2], plot_y[indices_diaplectic_k2], s=100, marker='+', c='r')

for fi in range(n_folder_free):
    plot_x = k_data_free[fi] 
    plot_y = r_data_free[fi]
    indices_symplectic = np.where(plot_y > .4)[0]
    indices_diaplectic = np.where(plot_y  < .4)[0]

    ax.scatter(plot_x[indices_symplectic], plot_y[indices_symplectic], s=50, marker='x', c='b')
    ax.scatter(plot_x[indices_diaplectic], plot_y[indices_diaplectic], s=50, marker='x', c='b')

    plot_y2 = avg_speed_along_axis_data_free[fi]
    ax2.scatter(plot_x[indices_symplectic], plot_y2[indices_symplectic], s=100, marker='+', c='black')
    ax2.scatter(plot_x[indices_diaplectic], plot_y2[indices_diaplectic], s=50, marker='x', c='b')
    
    plot_y3 = avg_rot_speed_along_axis_data_free[fi]
    ax3.scatter(plot_x[indices_symplectic], plot_y3[indices_symplectic], s=100, marker='+', c='black')
    ax3.scatter(plot_x[indices_diaplectic], plot_y3[indices_diaplectic], s=50, marker='x', c='b')


# ax.scatter(-1, -1, marker='+', c='r', label='Held fixed - Symplectic')
# ax.scatter(-1, -1, marker='x', c='r', label='Held fixed - Diaplectic')
# ax.scatter(-1, -1, marker='X', c='r', label='Held fixed - Diaplectic(#k=2)')
# ax.scatter(-1, -1, marker='+', c='b', label='Free - Symplectic')
# ax.scatter(-1, -1, marker='x', c='b', label='Free - Diaplectic')

# ax.scatter(-1, -1, marker='x', c='black', s=100, label='Symplectic')
# ax.scatter(-1, -1, marker='+', c='black', s=100, label='Diaplectic')
# ax.scatter(-1, -1, marker='P', c='black', s=100, label='Diaplectic(#k=2)')
ax.scatter(-1, -1, marker='+', c='r', s=100, label='Held fixed')
ax.scatter(-1, -1, marker='x', c='b', s=50, label='Free')

ax.set_xlabel(r'$k$')
ax.set_ylabel(r'$<r>$')
ax.set_ylim(0)
ax.set_xlim(0, 0.09)
ax.legend()

ax2.set_xlabel(r'$k$')
ax2.set_ylabel(r"$<V>T/L$")
ax2.scatter(None, None, marker='+', c='black', label='Symplectic')
ax2.scatter(None, None,  marker='x', c='b', label='Diaplectic')
ax2.legend()

ax3.set_xlabel(r'$k$')
ax3.set_ylabel(r"$<Ω>T$")
ax3.scatter(None, None, marker='+', c='black', label='Symplectic')
ax3.scatter(None, None,  marker='x', c='b', label='Diaplectic')
ax3.legend()


fig.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
fig.savefig(f'fig/order_parameter.pdf', bbox_inches = 'tight', format='pdf', transparent=True)
fig.savefig(f'fig/order_parameter.png', bbox_inches = 'tight', format='png', transparent=True)
fig2.savefig(f'fig/IVP_velocities_free.pdf', bbox_inches = 'tight', format='pdf', transparent=True)
fig3.savefig(f'fig/IVP_efficiencies_free.pdf', bbox_inches = 'tight', format='pdf', transparent=True)
plt.show()