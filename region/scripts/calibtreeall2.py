import numpy as np
from matplotlib import rc, gridspec
import matplotlib.pylab as plt
from scipy import loadtxt, optimize

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# Read in the data from file using "loadtxt()".
run, spem, spemErr, spes, occ, occErr, fitm = loadtxt('caliblogall.txt', unpack=True, skiprows=1)

spemErr = np.sqrt(spemErr)

spem_avg = np.mean(spem)
spem_rms = np.std(spem)

spes_avg = np.mean(spes)
spes_rms = np.std(spes)

fitm_avg = np.mean(fitm)
fitm_rms = np.std(fitm)

index = np.linspace(0, len(run)-1, len(run))

fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 2])

ax = fig.add_subplot(gs[0])
ax2= fig.add_subplot(gs[1], sharex=ax)

#ax.errorbar(index, spem, spemErr, fmt='bo', elinewidth=0.5, markeredgewidth=0.5, label='spe\_mean')
#ax.plot([-0.5, len(run)-0.5], [spem_avg,spem_avg], 'b-', label='Average')
#ax.fill_between([-0.5, len(run)-0.5], spem_avg + spem_rms, spem_avg - spem_rms, color='b', alpha=0.2, lw=0, label='spe\_mean RMS')
#ax.plot([],[], color='b', alpha=0.2, linewidth=10, label='spe\_mean RMS')

ax.errorbar(index, fitm, fmt='ro', elinewidth=0.5, markeredgewidth=0.5, label='gauss\_center')
ax.plot([-0.5, len(run)-0.5], [fitm_avg,fitm_avg], 'r-', label='Average')
ax.fill_between([-0.5, len(run)-0.5], fitm_avg + fitm_rms, fitm_avg - fitm_rms, color='r', alpha=0.2, lw=0, label='gauss\_center RMS')
ax.plot([],[], color='r', alpha=0.2, linewidth=10, label='gauss\_center RMS')

          #'spe\_mean Average: %.2f\n' \
          #'spe\_mean RMS: %.2f' \
textfit = 'gauss\_center Average: %.2f\n' \
          'gauss\_center RMS: %.2f' \
          % (fitm_avg, fitm_rms)

ax.text(0.30, 0.20, textfit, color='black', transform=ax.transAxes, 
        fontsize=20, verticalalignment='top', backgroundcolor='white',
        bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))

ax2.errorbar(index, spes, fmt='go', elinewidth=0.5, markeredgewidth=0.5, label='spe\_sigma')
ax2.plot([-0.5, len(run)-0.5], [spes_avg,spes_avg], 'g-', label='Average')
ax2.fill_between([-0.5, len(run)-0.5], spes_avg + spes_rms, spes_avg - spes_rms, color='g', alpha=0.2, lw=0, label='spe\_sigma RMS')
ax2.plot([],[], color='g', alpha=0.2, linewidth=10, label='spe\_sigma RMS')

textfit2 = 'spes\_sigma Average: %.2f\n' \
          'spes\_sigma RMS: %.2f' \
          % (spes_avg, spes_rms)

ax2.text(0.66, 0.32, textfit2, color='black', transform=ax2.transAxes, 
        fontsize=20, verticalalignment='top', backgroundcolor='white',
        bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))

xlabel = []
for j in range(0, len(run)):
    if j % 10 == 0:
        xlabel.append(run[j].astype(int))     

plt.xticks(np.arange(min(index), max(index)+1, 10.0), xlabel, rotation='horizontal')
#plt.xticks(index, run.astype(int), rotation='horizontal')
#plt.xticks(np.arange(min(index), max(index)+1, 10.0))

ax.set_title("gauss\_center")
ax2.set_title("spe\_sigma")

ax.set_xlim(-0.5, len(run)-0.5)
#ax2.set_xlim(-0.1, len(run)-0.9)

ax.set_xlabel('Run #')
ax.set_ylabel('gauss\_center [Count$\cdot$Samples]')
ax.legend(loc=(0.15, 0.70))
#legend = ax.legend(loc=(0.32,0.66))

ax2.set_xlabel('Run #')
ax2.set_ylabel('spe\_sigma [Count$\cdot$Samples]')
ax2.legend(loc='lower left')

plt.tight_layout()

plt.savefig('calibtreeall2.pdf')
plt.show()
