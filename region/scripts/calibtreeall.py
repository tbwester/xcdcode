import numpy as np
from matplotlib import rc, gridspec
import matplotlib.pylab as plt
from scipy import loadtxt, optimize

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# Read in the data from file using "loadtxt()".
run, spem, spemErr, spes, occ, occErr, fitm = loadtxt('caliblogall.txt', unpack=True, skiprows=1)

spemErr = np.sqrt(spemErr)
occErr = np.sqrt(occErr)

spem_avg = np.mean(spem)
spem_rms = np.std(spem)

occ_avg = np.mean(occ)
occ_rms = np.std(occ)

for j in range(0, len(spem)):
    if spem[j] > 120 or spem[j] < 100:
        print run[j]

index = np.linspace(0, len(run)-1, len(run))

fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 2])

ax = fig.add_subplot(gs[0])
ax2= fig.add_subplot(gs[1], sharex=ax)

ax.errorbar(index, spem, spemErr, fmt='bo', elinewidth=0.5, markeredgewidth=0.5, label='spe\_mean')
ax.plot([-0.5, len(run)-0.5], [spem_avg,spem_avg], 'b-', label='Average')
ax.fill_between([-0.5, len(run)-0.5], spem_avg + spem_rms, spem_avg - spem_rms, color='b', alpha=0.2, lw=0, label='RMS')
ax.plot([],[], color='b', alpha=0.2, linewidth=10, label='RMS')


textfit = 'spe\_mean Average: %.2f\n' \
          'spe\_mean RMS: %.2f' \
          % (spem_avg, spem_rms)

ax.text(0.71, 0.95, textfit, color='black', transform=ax.transAxes, 
        fontsize=20, verticalalignment='top', backgroundcolor='white',
        bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))


ax2.errorbar(index, occ, occErr, fmt='ro', elinewidth=0.5, markeredgewidth=0.5, label='occupancy')
ax2.plot([-0.5, len(run)-0.5], [occ_avg,occ_avg], 'r-', label='Average')
ax2.fill_between([-0.5, len(run)-0.5], occ_avg + occ_rms, occ_avg - occ_rms, color='r', alpha=0.2, lw=0, label='RMS')
ax2.plot([],[], color='r', alpha=0.2, linewidth=10, label='RMS')


textfit2 = 'occupancy Average: %.2f\n' \
          'occupancy RMS: %.2f' \
          % (occ_avg, occ_rms)

ax2.text(0.62, 0.95, textfit2, color='black', transform=ax2.transAxes, 
        fontsize=20, verticalalignment='top', backgroundcolor='white',
        bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))

xlabel = []
for j in range(0, len(run)):
    if j % 10 == 0:
        xlabel.append(run[j].astype(int))     

plt.xticks(np.arange(min(index), max(index)+1, 10.0), xlabel, rotation='horizontal')

#plt.xticks(index, run.astype(int), rotation='horizontal')

ax.set_title("spe\_mean")
ax2.set_title("Occupancy")

ax.set_xlim(-0.5, len(run)-0.5)
#ax2.set_xlim(-0.1, len(run)-0.9)

ax.set_xlabel('Run #')
ax.set_ylabel('spe\_mean [Count$\cdot$Samples]')
ax.legend(loc='upper left')
#legend = ax.legend(loc=(0.32,0.66))

ax2.set_xlabel('Run #')
ax2.set_ylabel('Occupancy')
ax2.legend(loc='upper left')

plt.tight_layout()

plt.savefig('calibtreeall.pdf')
plt.show()
