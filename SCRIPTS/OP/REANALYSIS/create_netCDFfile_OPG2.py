# A Python script for generating template netCDF file for OPG1
import netCDF4 as ncdf
import datetime as dt
import numpy as np
dir_work="../../REANALYSIS/OP_G2/"
dt_start=dt.datetime(2020,1,1,0,0,0) # Start date of output
dt_end=dt.datetime(2020,1,31,0,0,0)  # End date of output (for an initial test...terminate at 31/1/2020)
#dt_end=dt.datetime(2020,12,31,0,0,0)  # End date of output
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment

# You don't need to edit following part
type_name="daily";
fflag_tail="_OPG2_01_"+exp_name+".nc"
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

lon_out=np.arange(0,360,0.25)
lat_out=np.arange(-90,90.25,0.25)
#nfile=len(fnames_in)
missing=-9.99e33
ref_dt=dt.datetime(1900,1,1,0,0,0);time_units="days since "+str(ref_dt)

lonname="lon"
latname="lat"
timename="time"
for icycle in range(0,ncycle):
    dt_1=dt_start+dt.timedelta(days=icycle*nskip)
    dt_2=dt_start+dt.timedelta(days=(icycle+1)*nskip-1)
    time_out=np.asarray([(dt_1-ref_dt).days])
    print(dt_1,dt_2)
    for ivar in range(0,nvar):
        fname_out=dir_work+varnames_out[ivar]+"_"+str(dt_1.year*10000+dt_1.month*100+dt_1.day)+"_"+str(dt_2.year*10000+dt_2.month*100+dt_2.day)+fflag_tail
        # Create netCDF file
        nc_out=ncdf.Dataset(fname_out,"w")
        nc_out.createDimension(lonname,len(lon_out))
        nc_out.createDimension(latname,len(lat_out))
        nc_out.createDimension(timename,len(time_out))
        nc_out.createVariable(lonname,"float",[lonname])
        nc_out.createVariable(latname,"float",[latname])
        nc_out.createVariable(timename,"float",[timename])
        nc_out[lonname][:]=lon_out[:]
        nc_out[lonname].units="degrees_east"
        nc_out[latname][:]=lat_out[:]
        nc_out[latname].units="degrees_north"
        nc_out[timename][:]=time_out[:]
        nc_out[timename].units=time_units
        nc_out.createVariable(varnames_out[ivar],"float",[timename,latname,lonname])
        var_out=np.ones((len(time_out),len(lat_out),len(lon_out)))*missing
        nc_out.variables[varnames_out[ivar]].units=varunits[ivar]
        nc_out.variables[varnames_out[ivar]].long_name=varlong[ivar]
        nc_out.variables[varnames_out[ivar]].missing_value=missing
        nc_out.variables[varnames_out[ivar]][:]=var_out[:]
        nc_out.system_name=system_name
        nc_out.exp_name=exp_name
        nc_out.data_type=type_name
        nc_out.close()
 
