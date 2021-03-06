import numpy as np
from matplotlib import rc, gridspec, cm
import matplotlib.pylab as plt
from scipy import loadtxt, optimize

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# Read in the data from file using "loadtxt()".
run, spem, spemErr, spes, occ, occErr, fitm, drift, time = loadtxt('../data/caliblogalltime.txt', 
                                                      unpack=True, skiprows=1)

source = np.genfromtxt('../data/sourcelist.txt',dtype='str', delimiter='\t')

#The file stores the square of the uncertainty, so take the square root
spemErr = np.sqrt(spemErr)
occErr = np.sqrt(occErr)

#Calculate an average and rms for each population
spem_avg = np.mean(spem)
spem_rms = np.std(spem)

occ_avg = np.mean(occ)
occ_rms = np.std(occ)

#Get all the different drift fields
sources = []
for i in range(0,len(run)):
    if not source[i] in sources:
        sources.append(source[i])

sourceinfo = []
for m in range(0,len(sources)):
    sourcex = []
    sourcey = []
    sourceerr = []
    for q in range(0,len(run)):
        if source[q] == sources[m]:
            sourcex.append(time[q]) #run[q]
            sourcey.append(spem[q])
            sourceerr.append(spemErr[q])
    myvec = []
    myvec.append(sourcex)
    myvec.append(sourcey)
    myvec.append(sourceerr)
    sourceinfo.append(myvec)

#Index each run number
index = np.linspace(0, len(run)-1, len(run))

#Create plots
fig = plt.figure()
gs = gridspec.GridSpec(1, 1, height_ratios=[1, 0])

ax = fig.add_subplot(gs[0])
#ax2= fig.add_subplot(gs[1], sharex=ax)

#Plot the SPE mean for each drift field
color=iter(cm.rainbow(np.linspace(0,1,len(sources))))

for k in range(0, len(sourceinfo)):
    c=next(color)
    datalabel = 'spe\_mean (' + sources[k] + ')'
    ax.errorbar(sourceinfo[k][0], sourceinfo[k][1], sourceinfo[k][2], color=c, fmt='o', label=datalabel)

#Plot some elog events
ax.plot([40.03, 40.03], [105, 115], 'g--', linewidth=1.5)
ax.plot([41.25, 41.25], [105, 115], 'g--', linewidth=1.5)
ax.plot([41.52, 41.52], [105, 115], 'm--', linewidth=1.5)
ax.plot([41.6, 41.6], [105, 115], 'y--', linewidth=1.5)
ax.plot([44.12, 44.12], [105, 115], 'c--', linewidth=1.5)
ax.plot([45.13, 45.13], [105, 115], 'r--', linewidth=1.5)
ax.plot([44.835, 44.835], [105, 115], 'b--', linewidth=1.5)
ax.plot([46.04, 46.04], [105, 115], 'g--', linewidth=1.5)
text = 'Drift field increased \n wires moved \n Scroll pump on'
ax.text(0.49, 0.65, text, color='b', transform=ax.transAxes, fontsize=14)
text2 = '1\% filter \n removed'
ax.text(0.52, 0.16, text2, color='r', transform=ax.transAxes, fontsize=14)
text3 = 'Fan not in \n place?'
ax.text(0.01, 0.70, text3, color='g', transform=ax.transAxes, fontsize=14)
text4 = 'Fan replaced'
ax.text(0.025, 0.65, text4, color='g', transform=ax.transAxes, fontsize=14)
text5 = 'Lakeshore Crash'
ax.text(0.16, 0.16, text5, color='m', transform=ax.transAxes, fontsize=14)
text6 = 'Grid Voltage \n Power Loss?'
ax.text(0.17, 0.7, text6, color='y', transform=ax.transAxes, fontsize=14)
text7 = 'PMT Ramped \n Down to 1450V'
ax.text(0.29, 0.12, text7, color='c', transform=ax.transAxes, fontsize=14)
text8 = 'Source misaligned?'
ax.text(0.61, 0.12, text8, color='g', transform=ax.transAxes, fontsize=14)
text9 = 'Run \n 01497'
ax.text(0.01, 0.50, text9, color='k', transform=ax.transAxes, fontsize=14)

#Plot the RMS and add a dummy legend entry
#ax.fill_between([-0.5, len(run)-0.5], spem_avg + spem_rms, spem_avg - spem_rms, 
                #color='b', alpha=0.2, lw=0, label='RMS')
#ax.plot([],[], color='b', alpha=0.2, linewidth=10, label='RMS')


#textfit = 'spe\_mean Average: %.2f\n' \
          #'spe\_mean RMS: %.2f' \
          #% (spem_avg, spem_rms)

#ax.text(0.71, 0.95, textfit, color='black', transform=ax.transAxes, 
        #fontsize=20, verticalalignment='top', backgroundcolor='white',
        #bbox=dict(facecolor='white', edgecolor='lightgrey', pad=10.0))

#xlabel = []
#for j in range(0, len(run)):
#    if j % 10 == 0:
#        xlabel.append(run[j].astype(int))     

#plt.xticks(np.arange(min(index), max(index)+1, 10.0), xlabel, rotation='horizontal')

#plt.xticks(index, run.astype(int), rotation='horizontal')

ax.set_title("spe\_mean")
#ax2.set_title("Occupancy")

ax.set_xlim(40, 50)
ax.set_ylim(104, 117)
#ax2.set_xlim(-0.1, len(run)-0.9)

ax.set_xlabel('Days since First Run')
ax.set_ylabel('spe\_mean [Count$\cdot$Samples]')
ax.legend(loc='upper right', fontsize=10, ncol=2)
#legend = ax.legend(loc=(0.32,0.66))

#ax2.set_xlabel('Run #')
#ax2.set_ylabel('Occupancy')
#ax2.legend(loc='upper left')

plt.tight_layout()

plt.savefig('../plots/lasersourcetimecomments.pdf')
plt.show()
