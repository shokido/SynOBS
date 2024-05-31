# Python script for generating netCDF file for OP-G1
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../OP-FC"
dt_ini_start=dt.datetime(2020,1,6,0,0,0)# Start date of prediction
dt_ini_end=dt.datetime(2021,1,1,0,0,0)  # End date of prediction
y_not_leap=2021
institution_name="JAMSTEC"
contact_name="skido@jamstec.go.jp"
system_name="SAMPLE" # Name of your system
exp_names=["CNTL"]  # Name of experiments
version_name="0"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="OPF-P"
time_interp="pentad average fields"

nskip=5
dt_tmp=dt_ini_start
dts_ini=[dt_tmp]
while dt_tmp < dt_ini_end :
    year_tmp=dt_tmp.year
    dt_nl=dt_tmp.replace(year=y_not_leap)
    year_nl=dt_nl.year
    dt_nlp=dt_nl+dt.timedelta(days=nskip)
    year_nlp=dt_nlp.year
    year_tmp=year_tmp+year_nlp-year_nl
    dt_tmp=dt_nlp.replace(year=year_tmp)
    dts_ini.append(dt_tmp)
num_ini=len(dts_ini)
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
missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"

lonname="longitude"
latname="latitude"
levname="depth"
timename="juld"
for iexp in range(0,len(exp_names)):
    fflag_tail="_"+system_name+"_"+exp_names[iexp]+".nc"
    for inum in range(0,num_ini):
        nskip=5
        num_fcst=2
        dt_start=dts_ini[inum]
        initial_time=dt_start.strftime('%Y-%m-%d %H:%M:%S utc')
        dt_tmp=dt_start
        dts_pred=[dt_tmp]
        for icycle in range(0,num_fcst-1):
            year_tmp=dt_tmp.year
            dt_nl=dt_tmp.replace(year=y_not_leap)
            year_nl=dt_nl.year
            dt_nlp=dt_nl+dt.timedelta(days=nskip)
            year_nlp=dt_nlp.year
            year_tmp=year_tmp+year_nlp-year_nl
            dt_tmp=dt_nlp.replace(year=year_tmp)
            dts_pred.append(dt_tmp)
            
        for icycle in range(0,num_fcst):
            dt_pred=dts_pred[icycle]
            time_vstar=(dt_pred-ref_dt).days+(dt_pred-ref_dt).seconds/(60*60*24)
            time_out=np.asarray([time_vstar])
            leadtime_str='D'+'{:0>2d}'.format(icycle*nskip+1)
            leadtime_end='D'+'{:0>2d}'.format((icycle+1)*nskip)
            lead_time_out=np.asarray(['P'+str(icycle+1)+' ('+leadtime_str+'-' \
                            +leadtime_end+')'])
            for ivar in range(0,nvar):
                yyyymmdd=str(dt_start.year*10000+dt_start.month*100+dt_start.day)
                dir_name=dir_work+"/"+system_name+"/"+exp_names[iexp]+"/I"+str(yyyymmdd)+"/" \
                    +'/'+group_name+"/"+varnames_out[ivar]
                os.makedirs(dir_name,exist_ok=True)
                fname_out=dir_name+"/"+group_name+"_"+varnames_out[ivar] \
                    +"_I"+str(yyyymmdd)+'_P'+str(icycle+1)+fflag_tail
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
                nc_out[timename].long_name="Initial time of the valid pentad"
                nc_out[timename].units=time_units
                nc_out["lead_time"][:]=lead_time_out[:]
                nc_out["lead_time"].long_name="Lead time indices of the valid pentad and the first and last days of the pentad"
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

                title_name=project_name+" "+group_name+" "+varnames_out[ivar]+" Data"
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

