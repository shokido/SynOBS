import xarray as xr
from diag_libs import *
varname_temp="T";varname_lev="lev"

fnames_temp=[];fnames_out=[];temp_thres=[];varnames_out=[];varunits_out=[]
z_list=[17,20,26,28]
for i in range(0,len(z_list)):
    fnames_temp.append("../TestFile/T_20200101_GLOBAL_360x180.nc")
    temp_thres.append(z_list[i]);varnames_out.append("Z"+str(z_list[i]))
    fnames_out.append("Z"+str(z_list[i])+"_20200101_GLOBAL_360x180.nc")
    varunits_out.append("m")

for ifile in range(0,len(fnames_temp)):
    ds_temp=xr.open_dataset(fnames_temp[ifile])
    da_isoth= xr.apply_ufunc(
    find_isothern, 
    ds_temp[varname_temp], # temperature
    ds_temp[varname_lev], # depth
    input_core_dims=[['lev'], ['lev']],
    kwargs={'thres_var': temp_thres[ifile]},
    vectorize=True,  # Vectorize function over remaining 'x' and 'y' dimensions
    output_dtypes=[float],)
    ds_out=da_isoth.to_dataset(name=varnames_out[ifile])
    ds_out[varnames_out[ifile]].attrs["units"]=varunits_out[ifile]
    ds_out.to_netcdf(fnames_out[ifile])
