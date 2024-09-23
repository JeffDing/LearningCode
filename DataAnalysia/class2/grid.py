import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt 

gs = gridspec.GridSpec(3,3)

ax1 = plt.subplot(gs[0,:])
ax2 = plt.subplot(gs[1,:-1])
ax3 = plt.subplot(gs[1,:-1])
ax4 = plt.subplot(gs[2,0])
ax5 = plt.subplot(gs[2,1])