import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys
plt.rcParams.update({'font.size':18})
variable='tauu'
restofname='_trend_pvalue'

surf_path='/DataArchive/C3S/wind_stress'

ds = xr.open_dataset(surf_path+'/Results/'+'pvalue_'+variable+'_ORCA-0.25x0.25_regular_1979_2018.nc')
var = ds[variable+restofname]
meanvar = var.rename(r'$\tau_u~pvalue~\%$')

palette='Wistia'

fig = plt.figure(1, figsize=(15,8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = meanvar.plot.contourf(ax=ax, 
                 transform=ccrs.PlateCarree(),
                 extend='max',
                 vmin=0., vmax=100.,
                 #norm=colors.LogNorm(vmin=meanvar.min(), vmax=meanvar.max()),
                 cmap=palette,
                 levels=21,
                 cbar_kwargs={'shrink' : 0.80, 'drawedges': True})
ax.coastlines('50m')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+variable+'_pval_ORCA-0.25x0.25_regular_1979_2018.png', dpi=300, transparent=True)
plt.show()


