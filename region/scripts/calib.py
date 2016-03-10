import numpy as np
from matplotlib import rc, gridspec
import matplotlib.pylab as plt
from scipy import loadtxt, optimize

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# Read in the data from file using "loadtxt()".
index = np.linspace(0, 1000, 1001)
val = []
for i in range(0,1000):
    val.append( (1+index)*(0.99*(index+1) / index)**index )

val = np.asarray(val)

print val
