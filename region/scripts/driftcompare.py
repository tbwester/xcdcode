import numpy as np
from matplotlib import rc, gridspec, cm
import matplotlib.pylab as plt
from scipy import loadtxt, optimize

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# Read in the data from file using "loadtxt()".
run, spem, spemErr, spes, occ, occErr, fitm, drift = loadtxt('../data/caliblogall.txt', 
                                                      unpack=True, skiprows=1)

#The file stores the square of the uncertainty, so take the square root
spemErr = np.sqrt(spemErr)
occErr = np.sqrt(occErr)

#Calculate an average and rms for each population
spem_avg = np.mean(spem)
spem_rms = np.std(spem)

occ_avg = np.mean(occ)
occ_rms = np.std(occ)

#Get all the different drift fields
driftfields = []
for i in range(0,len(run)):
    if not drift[i] in driftfields:
        driftfields.append(drift[i])

#Sort drift fields ascending order
driftfields.sort()

driftinfo = []
for m in range(0,len(driftfields)):
    driftx = []
    drifty = []
    driftyerr = []
    for q in range(0,len(run)):
        if drift[q] == driftfields[m]:
            driftx.append(q) #run[q]
            drifty.append(spem[q])
            driftyerr.append(spemErr[q])
    myvec = []
    myvec.append(driftx)
    myvec.append(drifty)
    myvec.append(driftyerr)
    driftinfo.append(myvec)

#Index each run number
index = np.linspace(0, len(run)-1, len(run))

#Create plots
fig = plt.figure()
gs = gridspec.GridSpec(1, 1, height_ratios=[1, 0])

ax = fig.add_subplot(gs[0])
#ax2= fig.add_subplot(gs[1], sharex=ax)

#Plot the SPE mean for each drift field
color=iter(cm.rainbow(np.linspace(0,1,len(driftfields))))

for k in range(0, len(driftinfo)):
    c=next(color)
    datalabel = 'spe\_mean (%i V)' % (driftfields[k].astype(int))
    ax.errorbar(driftinfo[k][0], driftinfo[k][1], driftinfo[k][2], color=c, fmt='o', label=datalabel)
    #ax.plot([-0.5, len(run)-0.5], [spem_avg,spem_avg], 'b-', label='Average')

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

xlabel = []
for j in range(0, len(run)):
    if j % 10 == 0:
        xlabel.append(run[j].astype(int))     

plt.xticks(np.arange(min(index), max(index)+1, 10.0), xlabel, rotation='horizontal')

#plt.xticks(index, run.astype(int), rotation='horizontal')

ax.set_title("spe\_mean")
#ax2.set_title("Occupancy")

ax.set_xlim(-0.5, len(run)-0.5)
#ax2.set_xlim(-0.1, len(run)-0.9)

ax.set_xlabel('Run #')
ax.set_ylabel('spe\_mean [Count$\cdot$Samples]')
ax.legend(loc='upper right')
#legend = ax.legend(loc=(0.32,0.66))

#ax2.set_xlabel('Run #')
#ax2.set_ylabel('Occupancy')
#ax2.legend(loc='upper left')

plt.tight_layout()

plt.savefig('../plots/laserdrift.pdf')
plt.show()
