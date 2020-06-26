import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import sys
import running_mean as rm
from statsmodels.tsa.seasonal import seasonal_decompose
from mk_test import mk_test

plt.rcParams.update({'font.size':18})

variable='tau_modulus'
surf_path='/DataArchive/C3S/wind_stress'
low_lim=int(sys.argv[1])
high_lim=int(sys.argv[2])

ds = xr.open_dataset(surf_path+'/Results/tau_modulus_ORCA-0.25x0.25_regular_1979_2018.nc')
w = np.cos(ds.lat*np.pi/180.)
var = ds[variable]
#calculate latitudinal bands
lat_band = var.sel(lat=slice(low_lim, high_lim)).weighted(w.sel(lat=slice(low_lim, high_lim))).mean(dim=['lat', 'lon'])
n_months = len(ds.time)
n_years = int(n_months/12)
print(n_years)
## TREND ON ANNUAL TIME SERIES
frequency = 12*6
half_frequency = np.int(frequency/2.)
indexes=[np.array(range(i*12,(i+1)*12)).astype(int) for i in range(np.int(n_years))]
result = seasonal_decompose(lat_band, model='additive', filt=None, freq=frequency, two_sided=True, extrapolate_trend=0)
monthly_trend_component = result.trend[half_frequency:-half_frequency]
yearly_trend_component=[np.average(monthly_trend_component[indexes[t]]) for t in range(n_years-np.int(frequency/12))]
trend,h,p,z,slope,slope_conf = mk_test(yearly_trend_component, np.linspace(1,n_years-int(frequency/12),n_years-int(frequency/12)), True, 0.05)
print('Wind Stress_'+str(low_lim)+'_'+str(high_lim) + ' trend +- 2*std & test: ', slope, slope_conf*2.0, trend)


lat_band = rm.xr_running_mean(lat_band, 72)
lat_band = lat_band.rename(r'$Nm^{-2}$')
fig = plt.figure(1, figsize=(15,8))
ax = fig.add_subplot(111)
lat_band[3*12:-3*12].plot(ax=ax, label='6-year running mean', color='k')
ax.legend(loc='best')
fig.tight_layout()
fig.savefig(surf_path+'/Figures/tau_latband_'+str(low_lim)+'_'+str(high_lim)+'ts.png', dpi=300, transparent=True)
plt.show()



