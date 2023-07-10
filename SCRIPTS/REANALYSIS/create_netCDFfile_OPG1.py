# A Python script for generating template netCDF file for OPG1
import netCDF4 as ncdf
import datetime as dt
import numpy as np
dir_work="../../REANALYSIS/OP_G1/"
dt_start=dt.datetime(2020,1,1,0,0,0) # Start date of output
dt_end=dt.datetime(2020,1,31,0,0,0)  # End date of output (for an initial test...terminate at 31/1/2020)
#dt_end=dt.datetime(2020,12,31,0,0,0)  # End date of output
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment


# You don't need to edit following part
type_name="pentad"
fflag_tail="_OPG1_025_"+exp_name+".nc"
nskip=5
ncycle=int(((dt_end-dt_start).days+1)/nskip)
varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("SSH");vartypes.append("TLL");varlong.append("Sea surface height");varunits.append("m")
varnames_out.append("SIC");vartypes.append("TLL");varlong.append("Sea Ice Concentration Ratio");varunits.append("")
varnames_out.append("SIT");vartypes.append("TLL");varlong.append("Sea Ice Thickness");varunits.append("m")
varnames_out.append("Taux");vartypes.append("TLL");varlong.append("Zonal wind stress at the surface");varunits.append("N/m^2")
varnames_out.append("Tauy");vartypes.append("TLL");varlong.append("Meridional wind stress at the surface");varunits.append("N/m^2")
varnames_out.append("SWHF");vartypes.append("TLL");varlong.append("Shortwave (solar) heat flux at the sea surface;positive downward");varunits.append("W/m^2")
varnames_out.append("LWHF");vartypes.append("TLL");varlong.append("Longwave heat flux at the sea surface;positive downward");varunits.append("W/m^2")
varnames_out.append("SNHF");vartypes.append("TLL");varlong.append("Sensible heat flux at the sea surface;positive downward");varunits.append("W/m^2")
varnames_out.append("LAHF");vartypes.append("TLL");varlong.append("Latent heat flux at the sea surfac;positive downwarde");varunits.append("W/m^2")
varnames_out.append("NetHF");vartypes.append("TLL");varlong.append("Net heat flux at the sea surface;positive downward");varunits.append("W/m^2")
varnames_out.append("NetWF");vartypes.append("TLL");varlong.append("Net heat flux at the sea surface;positive downward");varunits.append("m/s")
varnames_out.append("T");vartypes.append("TLLL");varlong.append("Potential temperature with respect to 0m");varunits.append("Degree C")
varnames_out.append("S");vartypes.append("TLLL");varlong.append("Practical Salinity");varunits.append("psu")
varnames_out.append("U");vartypes.append("TLLL");varlong.append("Zonal Velocity");varunits.append("m/s")
varnames_out.append("V");vartypes.append("TLLL");varlong.append("Meridional Velocity");varunits.append("m/s")
nvar=len(varnames_out)

lon_out=np.arange(0,360,0.25)
lat_out=np.arange(-90,90.25,0.25)
lev_out=[1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, \
    220.0, 240.0, 270.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1350.0, \
        1500.0, 1750.0, 2000.0, 2500.0, 3000.0, 3500.0, 4000.0, 4500.0, 5000.0, 5500]
#nfile=len(fnames_in)
missing=-9.99e33
ref_dt=dt.datetime(1900,1,1,0,0,0);time_units="days since "+str(ref_dt)

lonname="lon";latname="lat";levname="lev";timename="time"
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
        nc_out.createVariable(lonname,"float32",[lonname])
        nc_out.createVariable(latname,"float32",[latname])
        nc_out.createVariable(timename,"float32",[timename])
        nc_out[lonname][:]=lon_out[:]
        nc_out[lonname].units="degrees_east"
        nc_out[latname][:]=lat_out[:]
        nc_out[latname].units="degrees_north"
        nc_out[timename][:]=time_out[:]
        nc_out[timename].units=time_units
        if (vartypes[ivar]=="TLLL"):
             nc_out.createDimension(levname,len(lev_out))
             nc_out.createVariable(levname,"float32",[levname])
             nc_out[levname][:]=lev_out
             nc_out[levname].units="m"
             nc_out.createVariable(varnames_out[ivar],"float32",[timename,levname,latname,lonname])
             var_out=np.ones((len(time_out),len(lev_out),len(lat_out),len(lon_out)))*missing
        else:
             nc_out.createVariable(varnames_out[ivar],"float32",[timename,latname,lonname])
             var_out=np.ones((len(time_out),len(lat_out),len(lon_out)))*missing
        nc_out.variables[varnames_out[ivar]].units=varunits[ivar]
        nc_out.variables[varnames_out[ivar]].long_name=varlong[ivar]
        nc_out.variables[varnames_out[ivar]].missing_value=missing
        nc_out.variables[varnames_out[ivar]][:]=var_out[:]
        nc_out.system_name=system_name
        nc_out.exp_name=exp_name
        nc_out.data_type=type_name
        nc_out.close()
 
