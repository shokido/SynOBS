# Python script for generating netCDF sample for S2S-G1
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../../S2S-AN"
dt_start=dt.datetime(2003,1,1,0,0,0) # Start date of output
dt_end=dt.datetime(2003,1,31,0,0,0)  # End date of output (for an initial test...terminate at 31/1/2003)
#dt_end=dt.datetime(2022,12,31,0,0,0)  # End date of output
institution_name="JMA-MRI"
contact_name="yfujii@mri-jma.go.jp"
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment
version_name="0"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="S2S-G1"
time_interp="daily average fields"
fflag_tail="_"+system_name+"_"+exp_name+".nc"
nskip=1
ncycle=int(((dt_end-dt_start).days+1)/nskip)
varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("SST");vartypes.append("TLL");varlong.append("Potential temperature at 1m");varunits.append("degree C")
varnames_out.append("SSS");vartypes.append("TLL");varlong.append("Practical salinity at 1m");varunits.append("psu")
varnames_out.append("SSU");vartypes.append("TLL");varlong.append("Zonal velocity at 1m");varunits.append("m/s")
varnames_out.append("SSV");vartypes.append("TLL");varlong.append("Meridional velocity at 1m");varunits.append("m/s")
varnames_out.append("SSH");vartypes.append("TLL");varlong.append("Sea surface height");varunits.append("m")
varnames_out.append("0-300mT");vartypes.append("TLL");varlong.append("Vertically averaged T between 0m and 300m");varunits.append("degree C")
varnames_out.append("Z20");vartypes.append("TLL");varlong.append("Depth of the 20 degree isotherm estimated from T.");varunits.append("m")
varnames_out.append("MLD001");vartypes.append("TLL");varlong.append("Mixed Layer Depth with the 0.05 density criteria");varunits.append("m")
varnames_out.append("0-300mS");vartypes.append("TLL");varlong.append("Vertically averaged S between 0m and 300m");varunits.append("degree C")
varnames_out.append("SIC");vartypes.append("TLL");varlong.append("Sea Ice Concentration ratio (0 to 1)");varunits.append("")
varnames_out.append("SIT");vartypes.append("TLL");varlong.append("Sea Ice Thickness");varunits.append("m")
varnames_out.append("0-50mT");vartypes.append("TLL");varlong.append("Vertically averaged T between 0m and 50m");varunits.append("degree C")
varnames_out.append("Z17");vartypes.append("TLL");varlong.append("Depth of the 17 degree isotherm estimated from T.");varunits.append("m")
varnames_out.append("Z26");vartypes.append("TLL");varlong.append("Depth of the 26 degree isotherm estimated from T.");varunits.append("m")
varnames_out.append("Z28");vartypes.append("TLL");varlong.append("Depth of the 28 degree isotherm estimated from T.");varunits.append("m")
varnames_out.append("TCHP");vartypes.append("TLL");varlong.append("Tropical Cyclone Heat Potential. Calculated as the oceanic heat content above Z26");varunits.append("kJ/cm^2")
varnames_out.append("MLD005");vartypes.append("TLL");varlong.append("Mixed Layer Depth with the 0.05 density criteria");varunits.append("m")
varnames_out.append("ILD05");vartypes.append("TLL");varlong.append("Isothermal Layer Depth with 0.5 degree temperature criteria");varunits.append("m")
varnames_out.append("SWHF");vartypes.append("TLL");varlong.append("Shortwave (solar) heat flux at the sea surface");varunits.append("W/m^2")
varnames_out.append("NetHF");vartypes.append("TLL");varlong.append("Net heat flux at the sea surface");varunits.append("W/m^2")
nvar=len(varnames_out)

lon_out=np.arange(0,360,1.0)
lat_out=np.arange(-90,90.25,1.0)
missing=-9.99E7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"

lonname="longitude"
latname="latitude"
timename="juld"

for icycle in range(0,ncycle):
    dt_1=dt_start+dt.timedelta(days=icycle*nskip)
    dt_2=dt_start+dt.timedelta(days=(icycle+1)*nskip-1)
    time_out=np.asarray([(dt_1-ref_dt).days])
    print(dt_1,dt_2)
    for ivar in range(0,nvar):
        yyyymm=dt_1.year*100+dt_1.month
        dir_name=dir_work+"/"+system_name+"/"+exp_name+"/"+group_name+"/" \
                  +varnames_out[ivar]+"/"+str(dt_1.year)
        os.makedirs(dir_name,exist_ok=True)
        fname_out=dir_name+"/"+group_name+"_"+varnames_out[ivar] \
          +"_"+str(yyyymm*100+dt_1.day)+fflag_tail

        # Create netCDF file
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
        nc_out.exp_name=exp_name
        nc_out.version=version_name
        nc_out.time_interp=time_interp
        nc_out.creation_date=creation_date
        nc_out.close()
 
