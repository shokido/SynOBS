import xarray as xr
from diag_libs import *
varname_temp="T";varname_lev="lev"
varname_salt="S"

fnames_temp=[];fnames_salt=[];fnames_out=[];dens_thres=[];varnames_out=[];varunits_out=[]
fnames_temp.append("../TestFile/T_20200101_GLOBAL_360x180.nc")
fnames_salt.append("../TestFile/S_20200101_GLOBAL_360x180.nc")
varnames_out.append("TCHP")
varunits_out.append("m")
fnames_out.append("TCHP_20200101_GLOBAL_360x180.nc")
for ifile in range(0,len(fnames_temp)):
    ds_temp=xr.open_dataset(fnames_temp[ifile])
    ds_salt=xr.open_dataset(fnames_salt[ifile])
    da_var= xr.apply_ufunc(
    find_tchp, 
    ds_temp[varname_temp], # temperature
    ds_salt[varname_salt], # salinity
    ds_temp[varname_lev], # depth
    input_core_dims=[['lev'],['lev'], ['lev']],
    vectorize=True,  # Vectorize function over remaining 'x' and 'y' dimensions
    output_dtypes=[float],)
    ds_out=da_var.to_dataset(name=varnames_out[ifile])
    ds_out[varnames_out[ifile]].attrs["units"]=varunits_out[ifile]
    ds_out.to_netcdf(fnames_out[ifile])
