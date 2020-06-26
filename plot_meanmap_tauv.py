import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys
plt.rcParams.update({'font.size':18})
variable='tauv'

surf_path='/DataArchive/C3S/wind_stress'

ds = xr.open_dataset(surf_path+'/Results/tauv_ORCA-0.25x0.25_regular_1979_2018.nc')
var = ds[variable]
meanvar = var.mean(dim='time').rename(r'$\tau_v~[Nm^{-2}]$')

fig = plt.figure(1, figsize=(9,4))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = meanvar.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), extend='both', 
                          vmin=-0.15, vmax=0.15, 
                          cmap='RdBu_r',
                          levels=31,
                          cbar_kwargs={'drawedges' : True})
ax.coastlines('50m')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+variable+'_meanmap_ORCA-0.25x0.25_regular_1979_2018_v1.png', dpi=300, transparent=True)
plt.show()

stdvar = var.groupby('time.year').mean('time').std(dim='year').rename(r'$\sigma_{\tau_v}~[Nm^{-2}]$')

fig = plt.figure(2, figsize=(9,4))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = stdvar.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), extend='max',                 
                 vmin=0., vmax=0.05, cmap='Wistia',
                 levels=21,
                 cbar_kwargs={'drawedges': True},   
                 infer_intervals=True)
ax.coastlines('50m')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+variable+'_stdmap_ORCA-0.25x0.25_regular_1979_2018_v1.png', dpi=300, transparent=True)
plt.show()

