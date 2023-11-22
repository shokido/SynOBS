import xarray as xr
from diag_libs import *
varname_lev="lev"
varnames_vel=[]
fnames_vel=[];fnames_out=[];vel_thres=[];varnames_out=[];varunits_out=[]

varnames_vel.append("U")
fnames_vel.append("../TestFile/U_20200101_GLOBAL_360x180.nc")
vel_thres.append(15.0);varnames_out.append("15mU")
varunits_out.append("m/s")
fnames_out.append("15mU_20200101_GLOBAL_360x180.nc")
varnames_vel.append("V")
fnames_vel.append("../TestFile/V_20200101_GLOBAL_360x180.nc")
vel_thres.append(15.0);varnames_out.append("15mV")
fnames_out.append("15mV_20200101_GLOBAL_360x180.nc")
varunits_out.append("m/s")

for ifile in range(0,len(fnames_vel)):
    ds_vel=xr.open_dataset(fnames_vel[ifile])
    # u=ds_vel[varnames_vel[ifile]][0,:,80,190]
    # print(np.shape(u))
    # print(np.shape(ds_vel[varname_lev]))
    # a=pcws_lagr1_multi(ds_vel[varname_lev].values,u.values,[20,30])
    # print(a)

    da_var= xr.apply_ufunc(
    pcws_lagr1, 
    ds_vel[varname_lev], # depth
    ds_vel[varnames_vel[ifile]], # Velocity
    input_core_dims=[['lev'], ['lev']],
    kwargs={'xx': vel_thres[ifile]},
    vectorize=True,  # Vectorize function over remaining 'x' and 'y' dimensions
    output_dtypes=[float],)
    ds_out=da_var.to_dataset(name=varnames_out[ifile])
    ds_out[varnames_out[ifile]].attrs["units"]=varunits_out[ifile]
    ds_out.to_netcdf(fnames_out[ifile])
