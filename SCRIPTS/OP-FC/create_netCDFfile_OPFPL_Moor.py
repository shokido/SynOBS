# Python script for generating netCDF file for OP-PL Moor
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../OP-FC"
dt_ini_start=dt.datetime(2020,1,6,0,0,0)# Start date of prediction
dt_ini_end=dt.datetime(2020,1,31,0,0,0)  # End date of prediction
#dt_ini_end=dt.datetime(2021,1,1,0,0,0)  # End date of prediction
institution_name="JAMSTEC"
contact_name="skido@jamstec.go.jp"
system_name="SAMPLE" # Name of your system
exp_names=["CNTL"]  # Name of experiments
version_name="0"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="OPF-PL"
plat_name="Mooring"
plat_short="Moor"
time_interp="hourly average value"

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

missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"


lonname="longitude"
latname="latitude"
levname="depth"
timename="juld"
posname="npoint"
for iexp in range(0,len(exp_names)):
    fflag_tail="_"+system_name+"_"+exp_names[iexp]+".nc"

    for inum in range(0,num_ini):
        dt_start=dts_ini[inum]
        initial_time=dt_start.strftime('%Y-%m-%d %H:%M:%S utc')
        dt_end=dt_start+dt.timedelta(days=10)

        yyyymmdd=str(dt_start.year*10000+dt_start.month*100+dt_start.day)
        dir_name=dir_work+"/"+system_name+"/"+exp_names[iexp]+"/I"+str(yyyymmdd) \
                +'/'+group_name+"/"+plat_short
        os.makedirs(dir_name,exist_ok=True)
        fname_out=dir_name+"/"+group_name+"_"+plat_short \
                +"_I"+str(yyyymmdd)+fflag_tail
        print(fname_out)

        dt_out=[]
        dt_now=dt_start
        while dt_now<dt_end:
            dt_out.append(dt_now)
            dt_now=dt_now+dt.timedelta(hours=1)
        time_out_day=[(i-ref_dt).days+(i-ref_dt).seconds/(60.0*60.0*24.0) for i in dt_out]
        lead_time_hour=[(i-dt_start).days*24+int((i-dt_start).seconds/(60.0*60.0))+1 for i in dt_out]
        time_out_lead=['H'+'{:0>3d}'.format(i) for i in lead_time_hour]
        #time_out_lead=[(i-dt_start).days+(i-dt_start).seconds/(60.0*60.0*24.0) for i in dt_out]

        nc_out=ncdf.Dataset(fname_out,"w")
        nc_out.createDimension(timename,len(time_out_day))
        nc_out.createDimension(posname,len(lon_point))
        nc_out.createDimension(levname,len(lev_out))
        nc_out.createVariable(levname,"float32",[levname])
        nc_out.createVariable(timename,"double",[timename])
        nc_out.createVariable(lonname,"float32",[posname])
        nc_out.createVariable(latname,"float32",[posname])
        nc_out.createVariable("lead_time","str",[timename])
        nc_out.variables[lonname].long_name="Longitude"
        nc_out.variables[lonname].units="degrees_east"
        nc_out.variables[lonname][:]=np.asarray(lon_point)
        nc_out.variables[latname].long_name="Latitude"
        nc_out.variables[latname].units="degrees_north"
        nc_out.variables[latname][:]=np.asarray(lat_point)
        nc_out.createVariable("Mooring_name","str",[posname])
        nc_out.variables[levname].long_name="Depths"
        nc_out[levname].units="m"
        nc_out[levname][:]=lev_out
        nc_out.variables[timename].long_name="initial time of the valid hour"
        nc_out.variables[timename].units=time_units
        nc_out.variables[timename][:]=np.asarray(time_out_day)

        nc_out.variables["lead_time"].long_name="Index of the valid hour"
        nc_out.variables["lead_time"][:]=np.asarray(time_out_lead)

        for ivar in range(0,nvar):
            if (vartypes[ivar]=="TLLL"):
                nc_out.createVariable(varnames_out[ivar],"float32",[timename,levname,posname])
                var_out=np.ones((len(time_out_day),len(lev_out),len(lon_point)))*missing
            else:
                nc_out.createVariable(varnames_out[ivar],"float32",[timename,posname])
                var_out=np.ones((len(time_out_day),len(lon_point)))*missing
            nc_out.variables[varnames_out[ivar]].units=varunits[ivar]
            nc_out.variables[varnames_out[ivar]].long_name=varlong[ivar]
            nc_out.variables[varnames_out[ivar]].missing_value=missing
            nc_out.variables[varnames_out[ivar]][:]=var_out[:]

        nc_out.variables["Mooring_name"][:]=mname[:]

        title_name=project_name+" "+group_name+" "+plat_name+" Data"
        nc_out.title=title_name
        nc_out.institution=institution_name
        nc_out.contact=contact_name
        nc_out.system=system_name
        nc_out.exp_name=exp_names[iexp]
        nc_out.initial_time=initial_time
        nc_out.version=version_name
        nc_out.time_interp=time_interp
        nc_out.creation_date=creation_date

        nc_out.close()
