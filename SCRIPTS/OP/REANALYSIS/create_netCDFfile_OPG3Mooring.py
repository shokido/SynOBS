# Python script for generating netCDF file for OPG3_Argo
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import calendar

dir_work="../../REANALYSIS/OP_G3Mooring/"
dt_start=dt.datetime(2020,1,1,0,0,0) # Start date of output
dt_end=dt.datetime(2020,1,31,0,0,0)  # End date of output (for an initial test...terminate at 31/1/2020)
#dt_end=dt.datetime(2020,12,31,0,0,0)  # End date of output
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment

# You don't need to edit following part
type_name="hourly";
fflag_tail="_OPG3Mooring_"+exp_name+".nc"
start_year=dt_start.year;start_month=dt_start.month
end_year=dt_end.year;end_month=dt_end.month
varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("T");vartypes.append("TLLL");varlong.append("Potential temperature with respect to 0m");varunits.append("Degree C")
varnames_out.append("S");vartypes.append("TLLL");varlong.append("Practical Salinity");varunits.append("psu")
varnames_out.append("U");vartypes.append("TLLL");varlong.append("Zonal Velocity");varunits.append("m/s")
varnames_out.append("V");vartypes.append("TLLL");varlong.append("Meridional Velocity");varunits.append("m/s")
varnames_out.append("SWHF");vartypes.append("TLL");varlong.append("Shortwave (solar) heat flux at the sea surface;positive downward");varunits.append("W/m^2")
varnames_out.append("NetHF");vartypes.append("TLL");varlong.append("Net heat flux at the sea surface;positive downward");varunits.append("W/m^2")
nvar=len(varnames_out)
start_year=2020;start_month=1
end_year=2020;end_month=12
dt_target=[]
for iy in range(start_year,end_year+1):
    if (iy==start_year):
        im1=start_month
    else:
        im1=1
    if (iy==end_year):
        im2=end_month+1
    else:
        im2=12+1
    for im in range(im1,im2):
        dt_target.append(dt.datetime(iy,im,1,0,0,0))

# You don't need to edit following part
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
print(mname)
missing=-9.99e33
ref_dt=dt.datetime(1900,1,1,0,0,0);time_units="days since "+str(ref_dt)
nfile=len(dt_target)

for ifile in range(0,nfile):
    yyyymm=dt_target[ifile].year*100+dt_target[ifile].month
    # Create netCDF file
    dt_str=dt.datetime(dt_target[ifile].year,dt_target[ifile].month,1,0,0,0)
    if (dt_target[ifile].month<12):
        dt_end=dt.datetime(dt_target[ifile].year,dt_target[ifile].month+1,1,0,0,0)
    else:
        dt_end=dt.datetime(dt_target[ifile].year+1,1,1,0,0,0)
    dt_out=[]
    dt_now=dt_str
    while dt_now<dt_end:
        dt_out.append(dt_now)
        dt_now=dt_now+dt.timedelta(hours=1)
    time_out_day=[(i-ref_dt).days+(i-ref_dt).seconds/(60.0*60.0*24.0) for i in dt_out]
    levname="lev";posname="pos";timename="time"
    for ivar in range(0,nvar):
        fname_out=dir_work+varnames_out[ivar]+"_"+str(yyyymm)+fflag_tail
        nc_out=ncdf.Dataset(fname_out,"w")
        nc_out.createDimension(timename,len(time_out_day))
        nc_out.createDimension(posname,len(lon_point))
        nc_out.createVariable(timename,"float",[timename])
        nc_out.createVariable("lon","float",[posname])
        nc_out.createVariable("lat","float",[posname])
        nc_out.createVariable("Mooring_name","str",[posname])
        nc_out.variables["lon"].long_name="longitude"
        nc_out.variables["lon"].units="degrees_east"
        nc_out.variables["lon"][:]=np.asarray(lon_point)
        nc_out.variables["lat"].long_name="latitude"
        nc_out.variables["lat"].units="degrees_north"
        nc_out.variables["lat"][:]=np.asarray(lat_point)
        nc_out.variables[timename].long_name="time"
        nc_out.variables[timename].units=time_units
        nc_out.variables[timename][:]=np.asarray(time_out_day)

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
        nc_out.variables[varnames_out[ivar]][:]=var_out[:]
        nc_out.variables["Mooring_name"][:]=mname[:]
        nc_out.system_name=system_name
        nc_out.exp_name=exp_name
        nc_out.data_type=type_name
        nc_out.close()
 
