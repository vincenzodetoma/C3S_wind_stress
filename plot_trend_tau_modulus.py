import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys
plt.rcParams.update({'font.size':18})
variable='tau_modulus'
restofname='_trend_matrix'

surf_path='/DataArchive/C3S/wind_stress'

ds = xr.open_dataset(surf_path+'/Results/'+'trend_'+variable+'_ORCA-0.25x0.25_regular_1979_2018.nc')
var = ds[variable+restofname]
meanvar = var.rename(r'$\tau~trend$'+'\n'+r'$[Nm^{-2}~{year}^{-1}]$')

palette='RdBu_r'

fig = plt.figure(1, figsize=(9,4))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = meanvar.plot.contourf(ax=ax, 
                 transform=ccrs.PlateCarree(),
                 extend='both',
                 vmin=-0.001, vmax=0.001,
                 #norm=colors.LogNorm(vmin=meanvar.min(), vmax=meanvar.max()),
                 cmap=palette,
                 levels=21,
                 cbar_kwargs={'drawedges': True})
ax.background_patch.set_facecolor('lightgrey') #instruction to have nans grey!!!!
ax.coastlines('50m')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+variable+'_trend_ORCA-0.25x0.25_regular_1979_2018.png', dpi=300, transparent=True)
plt.show()


