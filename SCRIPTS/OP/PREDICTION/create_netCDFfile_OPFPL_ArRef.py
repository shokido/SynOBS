# Python script for generating netCDF file for OP-PL Reference Argo
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
dir_argo="../../../Argo_Info/" # Path to files with "ArRefYYYYMM"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="OPF-PL"
plat_name="Reference Argo"
plat_short="ArRef"
time_interp="daily average value"
fflag_tail="_"+system_name+"_"+exp_name+".nc"

dts_ini=[]
ndays=int((dt_ini_end-dt_ini_start).days/5)+1
for i in range(0,ndays):
    dts_ini.append(dt_ini_start+dt.timedelta(days=i*5))
num_ini=len(dts_ini)
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"
lev_out=[1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 270.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1350.0, 1500.0, 1750.0, 2000.0]
missing=-9.99e7

lonname="longitude"
latname="latitude"
levname="depth"
timename="juld"
numname="numobs"

for inum in range(0,num_ini):
    dt_start=dts_ini[inum]
    initial_time=dt_start.strftime('%Y-%m-%d %H:%M:%S utc')
    dt_end=dt_start+dt.timedelta(days=10)
    nskip=5
    yyyymmdd=str(dt_start.year*10000+dt_start.month*100+dt_start.day)
    dir_name=dir_work+"/"+system_name+"/"+exp_name+"/I"+str(yyyymmdd)+"/" \
             +'/'+group_name+"/"+plat_short
    os.makedirs(dir_name,exist_ok=True)
    fname_out=dir_name+"/"+group_name+"_"+plat_short \
            +"_I"+str(yyyymmdd)+fflag_tail
    print(fname_out)

    dt_fcsts=[]
    yyyymm_fcst=[]
    for iday in range(0,(dt_end-dt_start).days):
        dt_f=dt_start+dt.timedelta(days=iday)
        dt_fcsts.append(dt_f)
        yyyymm_fcst.append(dt_f.year*100+dt_f.month)
    yyyymm_fcst_unique=list(set(yyyymm_fcst))   
    fnames_in=[dir_argo+plat_short+str(i) for i in yyyymm_fcst_unique]

    # Read Argo position data
    lon_out=[];lat_out=[];time_out=[]
    WMO_number=[];OBS_number=[];lead_time=[]
    obs_num_start=50000
    for ifile in range(0,len(fnames_in)):
        f=open(fnames_in[ifile],"r")
        lines=f.readlines()

        for iline in range(0,len(lines)):
            tmp=lines[iline]
            dt_tmp=dt.datetime(int(tmp[0:4]),int(tmp[4:6]),int(tmp[6:8]),int(tmp[9:11]),int(tmp[11:13]),0)
            if ((dt_tmp >= dt_start) and (dt_tmp<dt_end)):
                lat_tmp=float(tmp[14:19]);latf=tmp[19:20]
                lon_tmp=float(tmp[21:27]);lonf=tmp[27:28]
                if (latf=="S"):
                    lat=lat_tmp*(-1)
                else:
                    lat=lat_tmp
                if (lonf=="W"):
                    lon=360-lon_tmp
                else:
                    lon=lon_tmp
                lon_out.append(lon)
                lat_out.append(lat)
                time_out.append(dt_tmp)
                lead_time.append('D'+'{:0>2d}'.format((dt_tmp-dt_start).days+1))
                fflag=tmp[29:38].strip()
                WMO_number.append(fflag)
                OBS_number.append(obs_num_start+iline)
    #print(WMO_number)
    # Create netCDF file

    nprof=len(lon_out)
    nc_out=ncdf.Dataset(fname_out,"w")
    nc_out.createDimension(levname,len(lev_out))
    nc_out.createDimension(numname,len(OBS_number))
    nc_out.createVariable(levname,"float32",[levname])
    nc_out.variables[levname].long_name="Depths"
    nc_out.variables[levname].units="m"
    nc_out.variables[levname][:]=lev_out[:]
    nc_out.createVariable("T","float32",[numname,levname])
    nc_out.createVariable("S","float32",[numname,levname])
    nc_out.createVariable(timename,"double",[numname])
    nc_out.createVariable("lead_time","str",[numname])
    nc_out.createVariable(lonname,"float32",[numname])
    nc_out.createVariable(latname,"float32",[numname])
    WMO_number=np.asarray(WMO_number)
    nc_out.createVariable("WMO_number","str",[numname])
    nc_out.createVariable("OBS_number","int",[numname])
    time_out_day=[(i-ref_dt).days+(i-ref_dt).seconds/(60.0*60.0*24.0) for i in time_out]
    nc_out.variables[lonname].long_name="Longitude"
    nc_out.variables[latname].long_name="Latitude"
    nc_out.variables[timename].long_name="Observation time"
    nc_out.variables["lead_time"].long_name="Index of the valid day of the prediction"
    nc_out.variables["T"].long_name="Potential temperature"
    nc_out.variables["S"].long_name="Salinity"
    nc_out.variables["WMO_number"].long_name="WMO number"
    nc_out.variables["OBS_number"].long_name="Observation number"

    nc_out.variables[lonname].units="degrees_east"
    nc_out.variables[latname].units="degrees_north"
    nc_out.variables[timename].units=time_units
    nc_out.variables["T"].units="degrees celsius"
    nc_out.variables["S"].units="psu"

    nc_out.variables[lonname][:]=np.asarray(lon_out)
    nc_out.variables[latname][:]=np.asarray(lat_out)
    nc_out.variables[timename][:]=np.asarray(time_out_day)
    nc_out.variables["lead_time"][:]=np.asarray(lead_time)
    nc_out.variables["OBS_number"][:]=np.asarray(OBS_number)
    nc_out.variables["WMO_number"][:]=np.asarray(WMO_number)
    nc_out.variables["T"].long_name="Potential temperature"
    nc_out.variables["S"].long_name="Salinity"
    nc_out.variables["T"].missing_value=missing
    nc_out.variables["S"].missing_value=missing
    nc_out.variables["T"][:]=np.ones((len(OBS_number),len(lev_out)))*missing
    nc_out.variables["S"][:]=np.ones((len(OBS_number),len(lev_out)))*missing

    title_name=project_name+" "+group_name+" "+plat_name+" Data"
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
 
