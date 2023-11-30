# A Python script for generating template netCDF file for OP-G2H
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../OP-AN"
dt_start=dt.datetime(2020,1,1,0,0,0) # Start date of output
dt_end=dt.datetime(2020,1,31,0,0,0)  # End date of output (for an initial test...terminate at 31/1/2020)
#dt_end=dt.datetime(2020,12,31,0,0,0)  # End date of output
institution_name="JAMSTEC"
contact_name="skido@jamstec.go.jp"
system_name="SAMPLE" # Name of your system
exp_names=["CNTL"]  # Name of experiments
version_name="0"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="OP-G2H"
time_interp="daily average fields"
nskip=1
ncycle=int(((dt_end-dt_start).days+1)/nskip)
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
missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"

lonname="longitude"
latname="latitude"
timename="juld"
for iexp in range(0,len(exp_names)):
    fflag_tail="_"+system_name+"_"+exp_names[iexp]+".nc"
    for icycle in range(0,ncycle):
        dt_1=dt_start+dt.timedelta(days=icycle*nskip)
        dt_2=dt_start+dt.timedelta(days=(icycle+1)*nskip-1)
        time_out=np.asarray([(dt_1-ref_dt).days])
        print(dt_1,dt_2)
        for ivar in range(0,nvar):
            yyyymm=dt_1.year*100+dt_1.month
            dir_name=dir_work+"/"+system_name+"/"+exp_names[iexp]+"/"+group_name+"/" \
                      +varnames_out[ivar]+"/"+str(dt_1.year)
            os.makedirs(dir_name,exist_ok=True)
            fname_out=dir_name+"/"+group_name+"_"+varnames_out[ivar] \
              +"_"+str(yyyymm*100+dt_1.day)+fflag_tail

            nc_out=ncdf.Dataset(fname_out,"w")
            nc_out.createDimension(lonname,len(lon_out))
            nc_out.createDimension(latname,len(lat_out))
            nc_out.createDimension(timename,len(time_out))
            nc_out.createVariable(lonname,"float32",[lonname])
            nc_out.createVariable(latname,"float32",[latname])
            nc_out.createVariable(timename,"double",[timename])
            nc_out[lonname][:]=lon_out[:]
            nc_out[lonname].long_name="Longitude"
            nc_out[lonname].units="degrees_east"
            nc_out[latname][:]=lat_out[:]
            nc_out[latname].long_name="Latitude"
            nc_out[latname].units="degrees_north"
            nc_out[timename][:]=time_out[:]
            nc_out[timename].long_name="Initial time of the valid day"
            nc_out[timename].units=time_units
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
            nc_out.exp_name=exp_names[iexp]
            nc_out.version=version_name
            nc_out.time_interp=time_interp
            nc_out.creation_date=creation_date
            nc_out.close()
    
