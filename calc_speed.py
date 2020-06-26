import xarray as xr
import xarray.ufuncs as xu
import numpy as np
import matplotlib.pyplot as plt
import sys
import cartopy.crs as ccrs
import cmocean
plt.rcParams.update({'font.size': 14})

surf_path='/DataArchive/C3S/wind_stress'

dv = xr.open_dataset(surf_path+'/Results/'+'tauv_ORCA-0.25x0.25_regular_1979_2018.nc')
du = xr.open_dataset(surf_path+'/Results/'+'tauu_ORCA-0.25x0.25_regular_1979_2018.nc')
dv.coords['lon'] = (dv.coords['lon'] + 180) % 360 - 180
dv = dv.sortby(dv.lon)
du.coords['lon'] = (du.coords['lon'] + 180) % 360 - 180
du = du.sortby(du.lon)
v = dv['tauv'].squeeze()
u = du['tauu'].squeeze()
speed = xu.sqrt(u**2 + v**2)
speed = speed.rename('tau_modulus')
speed.to_netcdf(surf_path+'/Results/'+'tau_modulus_ORCA-0.25x0.25_regular_1979_2018.nc')

