# Python script for generating netCDF file for OPF-G2
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../../OP-FC"
dt_ini_start=dt.datetime(2020,1,6,0,0,0)# Start date of prediction
dt_ini_end=dt.datetime(2020,1,31,0,0,0)  # End date of prediction
#dt_ini_end=dt.datetime(2021,1,1,0,0,0)  # End date of prediction
institution_name="JAMSTEC"
contact_name="skido@jamstec.go.jp"
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment
version_name="0"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="OPF-G2"
time_interp="daily average fields"
fflag_tail="_"+system_name+"_"+exp_name+".nc"

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
lon_out=np.arange(0,360,0.25)
lat_out=np.arange(-90,90.25,0.25)
missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"

lonname="longitude"
latname="latitude"
levname="depth"
timename="juld"

for inum in range(0,num_ini):
    dt_start=dts_ini[inum]
    initial_time=dt_start.strftime('%Y-%m-%d %H:%M:%S utc')
    dt_end=dt_start+dt.timedelta(days=10)
    nskip=5
    num_fcst=int(((dt_end-dt_start).days+1)/nskip)
    leadtimes=np.asarray([1,3,7])
    num_fcst=len(leadtimes)
    for icycle in leadtimes:
      dt_pred=dt_start+dt.timedelta(days=int(icycle-1))
      time_vstar=(dt_pred-ref_dt).days+(dt_pred-ref_dt).seconds/(60*60*24)
      time_out=np.asarray([time_vstar])
      lead_time_out=np.asarray(['D'+'{:0>2d}'.format(icycle)])
      for ivar in range(0,nvar):
        yyyymmdd=str(dt_start.year*10000+dt_start.month*100+dt_start.day)
        dir_name=dir_work+"/"+exp_name+"/I"+str(yyyymmdd)+"/" \
             +'/'+group_name+"/"+varnames_out[ivar]
        os.makedirs(dir_name,exist_ok=True)
        fname_out=dir_name+"/"+group_name+"_"+varnames_out[ivar] \
            +"_I"+str(yyyymmdd)+'_D'+str(icycle)+fflag_tail
        print(fname_out)

        # Create netCDF file
        nc_out=ncdf.Dataset(fname_out,"w")
        nc_out.createDimension(lonname,len(lon_out))
        nc_out.createDimension(latname,len(lat_out))
        nc_out.createDimension(timename,len(time_out))
        nc_out.createVariable(lonname,"float32",[lonname])
        nc_out.createVariable(latname,"float32",[latname])
        nc_out.createVariable(timename,"double",[timename])
        nc_out.createVariable("lead_time","str",[timename])
        nc_out[lonname][:]=lon_out[:]
        nc_out[lonname].long_name="Longitude"
        nc_out[lonname].units="degrees_east"
        nc_out[latname][:]=lat_out[:]
        nc_out[latname].long_name="Latitude"
        nc_out[latname].units="degrees_north"
        nc_out[timename][:]=time_out[:]
        nc_out[timename].long_name="Initial time of the valid day"
        nc_out[timename].units=time_units
        nc_out["lead_time"][:]=lead_time_out[:]
        nc_out["lead_time"].long_name="Lead time index of the valid day"

        nc_out.createVariable(varnames_out[ivar],"float32",[timename,latname,lonname])
        var_out=np.ones((len(time_out),len(lat_out),len(lon_out)))*missing
        nc_out.variables[varnames_out[ivar]].units=varunits[ivar]
        nc_out.variables[varnames_out[ivar]].long_name=varlong[ivar]
        nc_out.variables[varnames_out[ivar]].missing_value=missing
        nc_out.variables[varnames_out[ivar]][:]=var_out[:]

        title_name=project_name+" "+group_name+" "+varnames_out[ivar]+" Data"
        nc_out.title=title_name
        nc_out.institution=institution_name
        nc_out.contact=contact_name
        nc_out.system=system_name
        nc_out.exp_name=exp_name
        nc_out.initial_time=initial_time
        nc_out.version=version_name
        nc_out.time_interp=time_interp
        nc_out.creation_date=creation_date

        nc_out.close()
