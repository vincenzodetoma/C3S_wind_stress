import xarray as xr
import xarray.ufuncs as xu
import numpy as np
import matplotlib.pyplot as plt
import sys
import cartopy.crs as ccrs
import cmocean
plt.rcParams.update({'font.size' :18})

surf_path='/DataArchive/C3S/wind_stress'
variable='curl'

dv = xr.open_dataset(surf_path+'/Results/'+'tauv_ORCA-0.25x0.25_regular_1979_2018.nc')
du = xr.open_dataset(surf_path+'/Results/'+'tauu_ORCA-0.25x0.25_regular_1979_2018.nc')
dv.coords['lon'] = (dv.coords['lon'] + 180) % 360 - 180
dv = dv.sortby(dv.lon)
du.coords['lon'] = (du.coords['lon'] + 180) % 360 - 180
du = du.sortby(du.lon)
v = dv['tauv'].squeeze()
u = du['tauu'].squeeze()
curl = (v.differentiate('lon') - u.differentiate('lat'))/(27.5*10**3)
curl_av = curl.mean(dim='time').rename(r'$\nabla\times\tau$'+'\n'+'[10'+r'$^{-7}~Nm^{-3}]$')*10**7

fig = plt.figure(1, figsize=(15,8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = curl_av.plot(ax=ax, transform=ccrs.PlateCarree(), extend='both',
                 vmin=-8.5, vmax=8.5,
                 cmap='RdBu_r',
                 cbar_kwargs={'shrink' : 0.80})
ax.coastlines('50m')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+variable+'_meancurl_ORCA-0.25x0.25_regular_1979_2018_v1.png', dpi=300, transparent=True)
plt.show()


