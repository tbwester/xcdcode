import numpy as np
from matplotlib import rc, gridspec
import matplotlib.pylab as plt
from scipy import loadtxt, optimize

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# Read in the data from file using "loadtxt()".
run, lhm, lhme, lhr, lhre, phm, phme, phr, phre, lfm, lfme, lfs, lfse, pfm, pfme, pfs, pfse, ks = loadtxt('log.txt', unpack=True, skiprows=1)

lfs = np.abs(lfs)
pfs = np.abs(pfs)

index = np.linspace(0, len(run)-1, len(run))

fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 2])

ax = fig.add_subplot(gs[0])
ax2= fig.add_subplot(gs[1], sharex=ax)

ax.errorbar(index, lhm, lhme, fmt='bo', elinewidth=0.5, markeredgewidth=0.5, label='Laser Hist')
ax.errorbar(index, phm, phme, fmt='ro', elinewidth=0.5, markeredgewidth=0.5, label='Pedestal Hist')

ax.errorbar(index, lfm, lfme, fmt='bo', elinewidth=0.5, markeredgewidth=0.5, alpha=0.4, label='Laser Fit')
ax.errorbar(index, pfm, pfme, fmt='ro', elinewidth=0.5, markeredgewidth=0.5, alpha=0.4, label='Pedestal Fit')

ax2.errorbar(index, lhr, lhre, fmt='bo', elinewidth=0.5, markeredgewidth=0.5, label='Laser RMS')
ax2.errorbar(index, phr, phre, fmt='ro', elinewidth=0.5, markeredgewidth=0.5, label='Pedestal RMS')

ax2.errorbar(index, lfs, lfse, fmt='bo', elinewidth=0.5, markeredgewidth=0.5, alpha=0.4, label='Laser Fit $\sigma$')
ax2.errorbar(index, pfs, pfse, fmt='ro', elinewidth=0.5, markeredgewidth=0.5, alpha=0.4, label='Pedestal Fit $\sigma$')

#ax.errorbar(index, ks, fmt='g-', label='KS Value')


plt.xticks(index, run.astype(int), rotation='horizontal')

ax.set_title("Region Mean Comparison")
ax2.set_title("Region RMS Comparison")

ax.set_xlim(-0.5, len(run)-0.5)
#ax.set_ylim(10,12)
#ax2.set_xlim(-0.1, len(run)-0.9)

ax.set_xlabel('Run #')
ax.set_ylabel('Mean')
ax.legend(loc='upper left')
#legend = ax.legend(loc=(0.32,0.66))

ax2.set_xlabel('Run #')
ax2.set_ylabel('RMS and $\sigma$')
ax2.legend(loc='upper right')

plt.tight_layout()

plt.savefig('calibrms.pdf')
plt.show()
