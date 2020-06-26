import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import sys
import running_mean as rm
plt.rcParams.update({'font.size':14})

variable='tau_modulus'
surf_path='/DataArchive/C3S/wind_stress'

ds = xr.open_dataset(surf_path+'/Results/tau_modulus_ORCA-0.25x0.25_regular_1979_2018.nc')
w = np.cos(ds.lat*np.pi/180.)
var = ds[variable]
#calculate global mean
globmean = var.weighted(w).mean(dim=['lat', 'lon'])
runn = rm.xr_running_mean(globmean, 72)
globmean = globmean.rename(r'$Nm^{-2}$')
#plot
fig = plt.figure(1, figsize=(9,6))
ax = fig.add_subplot(111)
globmean.plot(ax=ax, label='global mean', color='blue')
runn[3*12:-3*12].plot(ax=ax, label='6-year running mean', color='orange', linewidth=4)
ax.legend(loc='best')
ax.set_ylabel(globmean.name)
ax.set_xlabel(r'$time~[yr]$')
fig.tight_layout()
fig.savefig(surf_path+'/Figures/tau_globmean_ts.png', dpi=300, transparent=True)
plt.show()



