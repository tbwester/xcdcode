import numpy as np
from matplotlib import rc, gridspec
import matplotlib.pylab as plt
from scipy import loadtxt, optimize

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# Read in the data from file using "loadtxt()".
run, spem, spemErr, spes, occ, occErr, fitm = loadtxt('caliblog.txt', unpack=True, skiprows=0)
run2, spem2, spemErr2, spes2, occ2, occErr2, fitm2 = loadtxt('caliblog-3-3.txt', unpack=True, skiprows=0)
run3, spem3, spemErr3, spes3, occ3, occErr3, fitm3 = loadtxt('caliblog-3-6.txt', unpack=True, skiprows=0)

spemErr = np.sqrt(spemErr)
spemErr2 = np.sqrt(spemErr2)
spemErr3 = np.sqrt(spemErr3)

spem_avg = np.mean(spem)
spem_rms = np.std(spem)
spem_avg2 = np.mean(spem2)
spem_rms2 = np.std(spem2)
spem_avg3 = np.mean(spem3)
spem_rms3 = np.std(spem3)

index = np.linspace(0, len(run)-1, len(run))

print spem, spem2

fig = plt.figure()
gs = gridspec.GridSpec(1, 1, height_ratios=[1, 0])

ax = fig.add_subplot(gs[0])

ax.errorbar(index, spem, spemErr, fmt='bo', elinewidth=0.5, markeredgewidth=0.5, label='spe\_mean (0.33)')
ax.errorbar(index, spem2, spemErr2, fmt='ro', elinewidth=0.5, markeredgewidth=0.5, label='spe\_mean (0.25)')
ax.errorbar(index, spem3, spemErr3, fmt='go', elinewidth=0.5, markeredgewidth=0.5, label='spe\_mean (0.1)')

ax.plot([-0.5, len(run)-0.5], [spem_avg,spem_avg], 'b-', label='Average (0.33)')
ax.plot([-0.5, len(run)-0.5], [spem_avg2,spem_avg2], 'r-', label='Average (0.25)')
ax.plot([-0.5, len(run)-0.5], [spem_avg3,spem_avg3], 'g-', label='Average (0.1)')

#ax.fill_between([-0.5, len(run)-0.5], spem_avg + spem_rms, spem_avg - spem_rms, color='b', alpha=0.2, lw=0, label='RMS')
#ax.plot([],[], color='b', alpha=0.2, linewidth=10, label='RMS')

#ax.fill_between([-0.5, len(run)-0.5], spem_avg2 + spem_rms2, spem_avg2 - spem_rms2, color='r', alpha=0.2, lw=0, label='RMS')
#ax.plot([],[], color='r', alpha=0.2, linewidth=10, label='RMS 3-3')


textfit = 'spe\_mean (0.33) Average: %.3f\n' \
          'spe\_mean (0.33) RMS: %.3f' \
          % (spem_avg, spem_rms)

textfit2 = 'spe\_mean (0.25) Average: %.3f\n' \
           'spe\_mean (0.25) RMS: %.3f' \
           % (spem_avg2, spem_rms2)

textfit3 = 'spe\_mean (0.1) Average: %.3f\n' \
           'spe\_mean (0.1) RMS: %.3f' \
           % (spem_avg3, spem_rms3)

ax.text(0.15, 0.29, textfit, color='black', transform=ax.transAxes, 
        fontsize=16, verticalalignment='top', backgroundcolor='white',
        bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))

ax.text(0.15, 0.19, textfit2, color='black', transform=ax.transAxes, 
        fontsize=16, verticalalignment='top', backgroundcolor='white',
        bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))

ax.text(0.15, 0.09, textfit3, color='black', transform=ax.transAxes, 
        fontsize=16, verticalalignment='top', backgroundcolor='white',
        bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))


plt.xticks(index, run.astype(int), rotation='horizontal')

ax.set_title("spe\_mean")


ax.set_xlim(-0.5, len(run)-0.5)
#ax2.set_xlim(-0.1, len(run)-0.9)

ax.set_xlabel('Run #')
ax.set_ylabel('spe\_mean')
ax.legend(loc='upper left')
#legend = ax.legend(loc=(0.32,0.66))


plt.tight_layout()

plt.savefig('calibtree-3-4mean.pdf')
plt.show()
