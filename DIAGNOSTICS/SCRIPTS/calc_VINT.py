import xarray as xr
from diag_libs import *
import numpy as np
# Python script for vertical integration
varname_lev="lev"
varnames_in=[]
fnames_in=[];fnames_out=[];in_thres=[];varnames_out=[]
vint_1=[];vint_2=[]
varnames_in.append("T");fnames_in.append("../TestFile/T_20200101_GLOBAL_360x180.nc")
vint_1.append(0);vint_2.append(50);varnames_out.append("0-50mT")
varunits_out.append("degrees_celsius")
fnames_out.append("0-50mT_20200101_GLOBAL_360x180.nc")
varnames_in.append("T");fnames_in.append("../TestFile/T_20200101_GLOBAL_360x180.nc")
vint_1.append(0);vint_2.append(300);varnames_out.append("0-300mT")
varunits_out.append("degrees_celsius")
fnames_out.append("0-300mT_20200101_GLOBAL_360x180.nc")
varnames_in.append("S");fnames_in.append("../TestFile/S_20200101_GLOBAL_360x180.nc")
vint_1.append(0);vint_2.append(300);varnames_out.append("0-50mS")
varunits_out.append("PSU")
fnames_out.append("0-300mS_20200101_GLOBAL_360x180.nc")


dz=10
for ifile in range(0,len(fnames_in)):
    ds_in=xr.open_dataset(fnames_in[ifile])
    da_var= xr.apply_ufunc(
    cal_vint, 
    ds_in[varname_lev], # depth
    ds_in[varnames_in[ifile]], # inocity
    input_core_dims=[['lev'], ['lev']],
    kwargs={'x1': vint_1[ifile],'x2':vint_2[ifile], 'dx':dz},
    vectorize=True,  # Vectorize function over remaining 'x' and 'y' dimensions
    output_dtypes=[float],)
    da_var=da_var/(vint_2[ifile]-vint_1[ifile])
    ds_out=da_var.to_dataset(name=varnames_out[ifile])
    ds_out[varnames_out[ifile]].attrs["units"]=varunits_out[ifile]
    ds_out.to_netcdf(fnames_out[ifile])
