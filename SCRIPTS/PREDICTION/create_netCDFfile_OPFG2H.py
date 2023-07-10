# Python script for generating netCDF file for OPG1
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os
dir_work="../../PREDICTION/OPF_G2H/"
dt_ini_start=dt.datetime(2020,1,6,0,0,0)# Start date of prediction
dt_ini_end=dt.datetime(2020,1,31,0,0,0)  # End date of prediction
#dt_ini_end=dt.datetime(2021,1,1,0,0,0)  # End date of prediction
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment

# You don't need to edit following part
type_name="daily"
fflag_tail="_OPFG2H_01_"+exp_name+".nc"
dts_ini=[]
ndays=int((dt_ini_end-dt_ini_start).days/5)+1
for i in range(0,ndays):
    dts_ini.append(dt_ini_start+dt.timedelta(days=i*5))
num_ini=len(dts_ini)
varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("SSH");vartypes.append("TLL");varlong.append("Sea surface height");varunits.append("m")
varnames_out.append("SST");vartypes.append("TLL");varlong.append("Potential temperature at 1m");varunits.append("degree C")
varnames_out.append("SSS");vartypes.append("TLL");varlong.append("Practical salinity at 1m");varunits.append("psu")
varnames_out.append("SSU");vartypes.append("TLL");varlong.append("Zonal velocity at 1m");varunits.append("m/s")
varnames_out.append("SSV");vartypes.append("TLL");varlong.append("Meridional velocity at 1m");varunits.append("m/s")
varnames_out.append("0-50mT");vartypes.append("TLL");varlong.append("Vertically averaged T (It should be noted that T is potential temperature with respect to 0m) between 0m and 50m");varunits.append("degree C")
varnames_out.append("Z20");vartypes.append("TLL");varlong.append("Depth of the 20 degree isotherm estimated from T.");varunits.append("m")
varnames_out.append("Z26");vartypes.append("TLL");varlong.append("Depth of the 26 degree isotherm estimated from T.");varunits.append("m")
varnames_out.append("TCHP");vartypes.append("TLL");varlong.append("Tropical Cyclone Heat Potential (2D, Units in  kJ/cm^2). Calculated as the oceanic heat content above Z26");varunits.append("kJ/cm^2")
varnames_out.append("MLD005");vartypes.append("TLL");varlong.append("Mixed Layer Depth with the 0.05 density criteria (2D. Units in m). Depth at which the potential density with respect to 0m is 0.05kg/m^3 larger than the potential density calculated from SST and SSS).");varunits.append("m")
varnames_out.append("15mU");vartypes.append("TLL");varlong.append("Zonal Velocity at 15m depth");varunits.append("m/s")
varnames_out.append("15mV");vartypes.append("TLL");varlong.append("Meridional velocity at 15m depth");varunits.append("m/s")
nvar=len(varnames_out)
lon_out=np.arange(0,360,0.1)
lat_out=np.arange(-90,90.1,0.1)
missing=-9.99e33
ref_dt=dt.datetime(1900,1,1,0,0,0);time_units="days since "+str(ref_dt)
lonname="lon"
latname="lat"
levname="lev"
timename="numfcsts"

for inum in range(0,num_ini):
    dt_start=dts_ini[inum]
    dt_end=dt_start+dt.timedelta(days=10)
    nskip=5
    pred_flag=str(dt_start.year*10000+dt_start.month*100+dt_start.day)+"_"+str(dt_end.year*10000+dt_end.month*100+dt_end.day)
    # You don't need to edit following part
    num_fcst=int(((dt_end-dt_start).days+1)/nskip)
    dir_out=dir_work+pred_flag+"/"
    if (os.path.exists(dir_out)==False):
        os.makedirs(dir_out)

    leadtimes=np.asarray([1,3,7])
    num_fcst=len(leadtimes);time_out=[]
    for icycle in leadtimes:
        dt_pred=dt_start+dt.timedelta(days=icycle+0.5)
        time_out.append((dt_pred-ref_dt).days+(dt_pred-ref_dt).seconds/(60*60*24))
    for ivar in range(0,nvar):
        fname_out=dir_out+varnames_out[ivar]+"_"+pred_flag+fflag_tail
        print(fname_out)
        # Create netCDF file
        nc_out=ncdf.Dataset(fname_out,"w")
        nc_out.createDimension(lonname,len(lon_out))
        nc_out.createDimension(latname,len(lat_out))
        nc_out.createDimension(timename,num_fcst)
        nc_out.createVariable(lonname,"float",[lonname])
        nc_out.createVariable(latname,"float",[latname])
        nc_out.createVariable("time","float",[timename])
        nc_out.createVariable("leadtime","float",[timename])
        nc_out[lonname][:]=lon_out[:]
        nc_out[lonname].units="degrees_east"
        nc_out[latname][:]=lat_out[:]
        nc_out[latname].units="degrees_north"
        nc_out["time"][:]=time_out[:]
        nc_out["time"].units="days since "+str(ref_dt)
        nc_out["leadtime"][:]=leadtimes[:]
        nc_out.createVariable(varnames_out[ivar],"float",[timename,latname,lonname])
        var_out=np.ones((num_fcst,len(lat_out),len(lon_out)))*missing
        nc_out.variables[varnames_out[ivar]].units=varunits[ivar]
        nc_out.variables[varnames_out[ivar]].long_name=varlong[ivar]
        nc_out.variables[varnames_out[ivar]].missing_value=missing
        #nc_out.variables[varnames_out[ivar]][:]=var_out[:]
        nc_out.system_name=system_name
        nc_out.exp_name=exp_name
        nc_out.data_type=type_name
        nc_out.close()
