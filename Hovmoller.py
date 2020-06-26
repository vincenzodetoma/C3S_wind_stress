import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys
plt.rcParams.update({'font.size':14})
variable='tauu'

surf_path='/DataArchive/C3S/wind_stress'

ds = xr.open_dataset(surf_path+'/Results/tauu_ORCA-0.25x0.25_regular_1979_2018.nc')

var = ds[variable].sel(lat=slice(-5,5), lon=slice(130, 280))
var =  var - var.mean(dim='time')
weights = np.cos(ds.lat*np.pi/180).sel(lat=slice(-5,5))

hov_nino = var.weighted(weights).mean(dim='lat')
hov_nino = hov_nino.rename(r'$\tau_u~[Nm^{-2}]$'+'\n'+'Anomalies')
m = hov_nino.min().values.round(2)
M = hov_nino.max().values.round(2)
s = min(-m, M)
ran = 2*s
lev=np.linspace(-s, s, int(ran*1000) + 1).round(3)
#cont = hov_nino.where(hov_nino <= 34.)
fig=plt.figure(1, figsize=(8,10))
ax=fig.add_subplot(111)
p = hov_nino.plot.contourf(ax=ax, 
                  extend='both',
                  cmap='RdBu_r', 
                  #vmin=30.5, vmax=35.5, 
                  levels=lev[::5],
                  #norm=colors.LogNorm(vmin=hov_nino.min(), vmax=hov_nino.max()),
                  cbar_kwargs={'drawedges': True, 'ticks':lev[::5]})
#cont.plot.contour(ax=ax, vmin=33., vmax=34., levels=3, colors='k', add_colorbar=False)
fig.savefig(surf_path+'/Figures/'+variable+'_hovmoller_ORCA-0.25x0.25_regular_1979_2018_v1.png', dpi=300, transparent=True)
plt.show()

#Time series min and max

hov_min = hov_nino.min(dim='lon')
hov_max = hov_nino.max(dim='lon')
fig = plt.figure(1, figsize=(9,6))
ax = fig.add_subplot(111)
hov_min.plot(ax=ax, marker='o', color='green', label='min', markersize=4)
hov_max.plot(ax=ax, marker='^', color='blue', label='max', markersize=4)
ax.legend(loc='best')
ax.set_xlabel(r'$time~[yr]$')
ax.set_ylabel(r'$Anomalies~[Nm^{-2}]$')
fig.tight_layout()
fig.savefig(surf_path+'/Figures/'+variable+'_minmax_hovmoller_ORCA-0.25x0.25_regular_1979_2018_v1.png', dpi=300, transparent=True)
plt.show()

