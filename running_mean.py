import xarray as xr
import numpy as np

def xr_running_mean(vec, win):
   b = int(win/2)
   new = xr.DataArray(np.zeros(len(vec)), coords=vec.coords, dims=vec.dims, name='run_mean'+str(win)+str(vec.name)) 
   for i in range(len(vec)):
     new[i] = vec[max(0,i-b):min(len(vec),i+b)].mean()
   return new

def running_mean(vec, win):
   b = int(win/2)
   new = np.zeros(len(vec))
   for i in range(len(vec)):
     new[i] = vec[max(0,i-b):min(len(vec),i+b)].mean()
   return new

def calc_entropy(T1,T2,T3, kk, jj):
    from itertools import product
    print(kk,jj)
    amoc_oras5 = T1.isel(lat=kk, lon=jj)
    other_var = T2.isel(lat=kk, lon=jj)
    another_var = T3.isel(lat=kk, lon=jj)
    test = ~np.isnan(amoc_oras5).all()
    if(test):
      ys = amoc_oras5.time.dt.year.values[0]
      ye = amoc_oras5.time.dt.year.values[-1] +1
      amoc_oras5 = np.asarray(amoc_oras5.squeeze())
      amoc_oras5 = (amoc_oras5 - amoc_oras5.mean()) / amoc_oras5.std()
      other_var = np.asarray(other_var.squeeze())
      other_var = (other_var - other_var.mean()) / other_var.std()
      another_var = np.asarray(another_var.squeeze())
      another_var = (another_var - another_var.mean()) / another_var.std()
      #Embedding of the time series in its phase space
      lag=1
      N = len(amoc_oras5)
      N3 = int(N/(lag))
      x = amoc_oras5
      y = other_var
      z = another_var
      idx = np.linspace(0.0,1.0,N3)
      #plot of the embedded time series
      #fig = plt.figure(1, figsize=(10,8))
      #ax = fig.add_subplot(111, projection='3d')
      #cset1 = ax.scatter(x,y,z, c=cm.winter(idx))
      #cset1.set_cmap('winter')
      #cbar = fig.colorbar(cset1, ax=ax)
      #cbar.ax.set_yticklabels(np.linspace(ys,ye,6).astype(int))
      #ax.set_title('Embedding of the RAPID 26.5N Time Series')
      #fig.tight_layout()
      #fig.savefig('recurrence_plots/embedding_rapid_amoc.png', dpi=300, transparent=True)
      #plt.show()
      #Recurrence plot construction
      treshold = 1 #treshold of tot Sv
      R = np.zeros((N3, N3))
      for i in range(N3):
        for j in range(N3):
          d = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2 + (z[i] - z[j])**2)
          if(d<treshold):
            R[i,j] = 1
      #fig=plt.figure(1, figsize=(10,10))
      #ax= fig.add_subplot(111)
      #time = np.linspace(ys, ye, N3)
      #im = ax.contourf(time, time, R, cmap='Blues', levels=1)
      #cbar = fig.colorbar(im, ax=ax, fraction=0.046)
      #ax.set_xlabel('Time')
      #ax.set_ylabel('Time')
      #ax.set_title('RAPID Recurrence Plot')
      #fig.tight_layout()
      #fig.savefig('recurrence_plots/rapid_recurrplot.png', dpi=300, transparent=True)
      #plt.show()
      M=2
      num_M = 2**M**2
      prob = np.zeros(num_M)
      baselist = [1]
      baselist.extend([0]* (M - len(baselist)))
      cases = product(baselist, repeat=M*M)
      cases = np.reshape(list(cases), (-1, M, M))
      s_max = np.log(num_M)
      S = 0
      num_samples = 10000
      draws = [np.random.choice(R.reshape(N3*N3), size=(M,M)) for i in range(num_samples)]
      for i in range(len(prob)):
        for ii in range(len(draws)):
          if(cases[i] == draws[ii]).all():
            prob[i] = prob[i] + 1/num_samples
      #print(prob.sum())
      S = -(prob*np.log(prob)).sum() / s_max
    else:
      S = np.nan
    #ENTR[kk,jj] = S
    #print(kk,jj, S)
    return S
