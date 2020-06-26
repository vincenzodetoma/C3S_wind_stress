# C3S_wind_stress
This repository contains the metrics used to produce the figures for the C3S_511 wind stress assessment report
In particular, here's the list of what each script does:
plot_meanmap_tau*.py -> plot the climatology and interannual variability for selected variables
calc_speed.py -> calculation of the modulus of the wind stress
trend_tau*.py -> calculation of the trend, with mk_kendall test for the masking of low p-value regions;
plot_trend_tau*.py -> plot the map of the linear trend
globmean.py -> calculates and plot global average time series
lat_bands.py -> calculate and show the latitudinal band-averaged time series with trend estimation
arrow_plot.py -> makes the plot with streamvector for the components and colormap for the modulus
wind_stress_curl.py -> calculation of the curl of the wind stress.py
Hovmoller.py -> extraction of the Hovmoller diagram in the El-Nino region, together with the max_min indicator.
All other scripts are ancillary code to let all the rest to work properly. 
Masked value in the trend map are controlled by a treshold to set in slice_trend.py:
trend,h,p,z,slope,std_conf = mk_test(yearly_trend_component, np.linspace(1,n_years_trend_component,n_years_trend_component), False, 0.05),
the last argument meaning that all values which have a % p-value lower than 95% are masked with nan values, because the trend estimate is not statistically significant.
