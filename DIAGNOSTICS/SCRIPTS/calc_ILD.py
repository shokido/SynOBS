import xarray as xr
from diag_libs import *
varname_temp="T";varname_lev="lev"
varname_salt="S"

fnames_temp=[];fnames_out=[];temp_thres=[];varnames_out=[]
fnames_temp.append("../TestFile/T_20200101_GLOBAL_360x180.nc")
temp_thres.append(0.5);varnames_out.append("ILD05")
fnames_out.append("ILD05_20200101_GLOBAL_360x180.nc")

for ifile in range(0,len(fnames_temp)):
    ds_temp=xr.open_dataset(fnames_temp[ifile])
    da_var= xr.apply_ufunc(
    find_ild, 
    ds_temp[varname_temp], # temperature
    ds_temp[varname_lev], # depth
    input_core_dims=[['lev'],['lev']],
    kwargs={'thres_temp': temp_thres[ifile]},
    vectorize=True,  # Vectorize function over remaining 'x' and 'y' dimensions
    output_dtypes=[float],)
    ds_out=da_var.to_dataset(name=varnames_out[ifile])
    ds_out.to_netcdf(fnames_out[ifile])
