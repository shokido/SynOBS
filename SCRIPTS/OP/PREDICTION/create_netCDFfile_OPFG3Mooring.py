# Python script for generating netCDF file for OPG1
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../PREDICTION/OPF_G3Mooring/"
dt_ini_start=dt.datetime(2020,1,6,0,0,0)# Start date of prediction
dt_ini_end=dt.datetime(2020,1,31,0,0,0)  # End date of prediction
#dt_ini_end=dt.datetime(2021,1,1,0,0,0)  # End date of prediction
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment

# You don't need to edit following part
type_name="hourly"
fflag_tail="_OPFG3Mooring_"+exp_name+".nc"
dts_ini=[]
ndays=int((dt_ini_end-dt_ini_start).days/5)+1
for i in range(0,ndays):
    dts_ini.append(dt_ini_start+dt.timedelta(days=i*5))
num_ini=len(dts_ini)

varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("T");vartypes.append("TLLL");varlong.append("Potential temperature with respect to 0m");varunits.append("Degree C")
varnames_out.append("S");vartypes.append("TLLL");varlong.append("Practical Salinity");varunits.append("psu")
varnames_out.append("U");vartypes.append("TLLL");varlong.append("Zonal Velocity");varunits.append("m/s")
varnames_out.append("V");vartypes.append("TLLL");varlong.append("Meridional Velocity");varunits.append("m/s")
varnames_out.append("SWHF");vartypes.append("TLL");varlong.append("Shortwave (solar) heat flux at the sea surface;positive downward");varunits.append("W/m^2")
varnames_out.append("NetHF");vartypes.append("TLL");varlong.append("Net heat flux at the sea surface;positive downward");varunits.append("W/m^2")
nvar=len(varnames_out)

lev_out=[1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 270.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
mname=["0-110W", "0-140W", "0-170W", "0-165E", "0-156E", "1S-140W", "1N-140W", "30.32S-71.76W", "13N-137E", "2N-140W"]
lon_point=[];lat_point=[]
for i in range(0,len(mname)):
    tmp=mname[i].split("-")
    print(tmp)
    latp=tmp[0]
    lonp=tmp[1]
    if (latp[-1]=="N"):
        latp=float(latp[0:len(latp)-1])
    elif (latp[-1]=="S"):
        latp=-1*float(latp[0:len(latp)-1])
    else:
        latp=float(latp)
    lat_point.append(latp)
    if (lonp[-1]=="W"):
        lonp=360-float(lonp[0:len(lonp)-1])
    elif (lonp[-1]=="E"):
        lonp=float(lonp[0:len(lonp)-1])
    lon_point.append(lonp)
mname=np.asarray(mname)
missing=-9.99e33
ref_dt=dt.datetime(1900,1,1,0,0,0);time_units="days since "+str(ref_dt)
# lonname="lon"
# latname="lat"
# levname="lev"
# timename="numfcsts"

for inum in range(0,num_ini):
    dt_start=dts_ini[inum]
    dt_end=dt_start+dt.timedelta(days=10)
    pred_flag=str(dt_start.year*10000+dt_start.month*100+dt_start.day)+"_"+str(dt_end.year*10000+dt_end.month*100+dt_end.day)
    # You don't need to edit following part
    dir_out=dir_work+pred_flag+"/"
    if (os.path.exists(dir_out)==False):
        os.makedirs(dir_out)

    dt_out=[]
    dt_now=dt_start
    while dt_now<dt_end:
        dt_out.append(dt_now)
        dt_now=dt_now+dt.timedelta(hours=1)
    time_out_day=[(i-ref_dt).days+(i-ref_dt).seconds/(60.0*60.0*24.0) for i in dt_out]
    time_out_lead=[(i-dt_start).days+(i-dt_start).seconds/(60.0*60.0*24.0) for i in dt_out]
    levname="lev";posname="pos";timename="numfcsts"

    for ivar in range(0,nvar):
        fname_out=dir_out+varnames_out[ivar]+"_"+pred_flag+fflag_tail
        print(fname_out)

        nc_out=ncdf.Dataset(fname_out,"w")
        nc_out.createDimension(timename,len(time_out_day))
        nc_out.createDimension(posname,len(lon_point))
        nc_out.createVariable(timename,"float",[timename])
        nc_out.createVariable("lon","float",[posname])
        nc_out.createVariable("lat","float",[posname])
        nc_out.createVariable("leadtime","float",[timename])
        nc_out.variables["lon"].long_name="longitude"
        nc_out.variables["lon"].units="degrees_east"
        nc_out.variables["lon"][:]=np.asarray(lon_point)
        nc_out.variables["lat"].long_name="latitude"
        nc_out.variables["lat"].units="degrees_north"
        nc_out.variables["lat"][:]=np.asarray(lat_point)
        nc_out.createVariable("Mooring_name","str",[posname])
        nc_out.variables[timename].long_name="time"
        nc_out.variables[timename].units=time_units
        nc_out.variables[timename][:]=np.asarray(time_out_day)

        nc_out.variables["leadtime"].long_name="time"
        nc_out.variables["leadtime"].units="days since "+str(dt_start)
        nc_out.variables["leadtime"][:]=np.asarray(time_out_lead)

        if (vartypes[ivar]=="TLLL"):
             nc_out.createDimension(levname,len(lev_out))
             nc_out.createVariable(levname,"float",[levname])
             nc_out[levname][:]=lev_out
             nc_out[levname].units="m"
             nc_out.createVariable(varnames_out[ivar],"float",[timename,levname,posname])
             var_out=np.ones((len(time_out_day),len(lev_out),len(lon_point)))*missing
        else:
             nc_out.createVariable(varnames_out[ivar],"float",[timename,posname])
             var_out=np.ones((len(time_out_day),len(lon_point)))*missing
        nc_out.variables[varnames_out[ivar]].units=varunits[ivar]
        nc_out.variables[varnames_out[ivar]].long_name=varlong[ivar]
        nc_out.variables[varnames_out[ivar]].missing_value=missing
        nc_out.variables["Mooring_name"][:]=mname[:]
        nc_out.variables[varnames_out[ivar]][:]=var_out[:]
        nc_out.system_name=system_name
        nc_out.exp_name=exp_name
        nc_out.data_type=type_name
        nc_out.close()


        # # Create netCDF file
        # nc_out=ncdf.Dataset(fname_out,"w")
        # nc_out.createDimension(lonname,len(lon_out))
        # nc_out.createDimension(latname,len(lat_out))
        # nc_out.createDimension(timename,num_fcst)
        # nc_out.createVariable(lonname,"float",[lonname])
        # nc_out.createVariable(latname,"float",[latname])
        # nc_out.createVariable("time_mid","float",[timename])
        # nc_out.createVariable("leadtime_str","float",[timename])
        # nc_out.createVariable("leadtime_end","float",[timename])
        # nc_out[lonname][:]=lon_out[:]
        # nc_out[lonname].units="degrees_east"
        # nc_out[latname][:]=lat_out[:]
        # nc_out[latname].units="degrees_north"
        # nc_out["time_mid"][:]=time_mid
        # nc_out["time_mid"].units="days since "+str(ref_dt)
        # nc_out["leadtime_str"][:]=leadtime_str[:]
        # nc_out["leadtime_end"][:]=leadtime_end[:]
        # if (vartypes[ivar]=="TLLL"):
        #     nc_out.createDimension(levname,len(lev_out))
        #     nc_out.createVariable(levname,"float",[levname])
        #     nc_out[levname][:]=lev_out
        #     nc_out[levname].units="m"
        #     nc_out.createVariable(varnames_out[ivar],"float",[timename,levname,latname,lonname])
        #     var_out=np.ones((num_fcst,len(lev_out),len(lat_out),len(lon_out)))*missing
        # else:
        #     nc_out.createVariable(varnames_out[ivar],"float",[timename,latname,lonname])
        #     var_out=np.ones((num_fcst,len(lat_out),len(lon_out)))*missing
        # nc_out.variables[varnames_out[ivar]].units=varunits[ivar]
        # nc_out.variables[varnames_out[ivar]].long_name=varlong[ivar]
        # nc_out.variables[varnames_out[ivar]].missing_value=missing
        # #nc_out.variables[varnames_out[ivar]][:]=var_out[:]
        # nc_out.system_name=system_name
        # nc_out.exp_name=exp_name
        # nc_out.data_type=type_name
        # nc_out.close()
