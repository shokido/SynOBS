# Python script for generating netCDF file for OPG3_Argo
import netCDF4 as ncdf
import datetime as dt
import numpy as np
dir_work="../../REANALYSIS/OP_G3Argo/"
dt_start=dt.datetime(2020,1,1,0,0,0) # Start date of output
dt_end=dt.datetime(2020,1,31,0,0,0)  # End date of output (for an initial test...terminate at 31/1/2020)
dt_end=dt.datetime(2020,12,31,0,0,0)  # End date of output
system_name="SAMPLE" # Name of your system
exp_name="CNTL"  # Name of experiment
dir_argo="../../../ARGOINFO/" # Path to files with "ArRefYYYYMM"

# You don't need to edit following part
type_name="daily";
fflag_tail="_OPG3ARGO_"+exp_name+".nc"
missing=-9.99e33
ref_dt=dt.datetime(1900,1,1,0,0,0);time_units="days since "+str(ref_dt)
lev_out=[1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 270.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1350.0, 1500.0, 1750.0, 2000.0]

start_year=dt_start.year;start_month=dt_start.month
end_year=dt_end.year;end_month=dt_end.month
fnames_Argo=[]
fnames_out=[]
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
        fnames_Argo.append(dir_argo+"ArRef"+str(iy*100+im))
        fnames_out.append(dir_work+"TSRef_"+str(iy*100+im)+fflag_tail)
        fnames_Argo.append(dir_argo+"ArAsm"+str(iy*100+im))
        fnames_out.append(dir_work+"TSAsm_"+str(iy*100+im)+fflag_tail)

nfile=len(fnames_Argo)

for ifile in range(0,nfile):
    f=open(fnames_Argo[ifile],"r")
    lines=f.readlines()

    lon_out=[];lat_out=[];time_out=[]
    WMO_number=[];OBS_number=[];OBS_yyyymm=[]
    obs_num_start=50000
    for iline in range(0,len(lines)):
        tmp=lines[iline]
        dt_tmp=dt.datetime(int(tmp[0:4]),int(tmp[4:6]),int(tmp[6:8]),int(tmp[9:11]),int(tmp[11:13]),0)
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
        fflag=tmp[29:38].strip()
        WMO_number.append(fflag)
        OBS_number.append(obs_num_start+iline)
        OBS_yyyymm.append(dt_tmp.year*100+dt_tmp.month)
    # Create netCDF file
    nprof=len(lon_out)
    levname="lev";numname="num"
    nc_out=ncdf.Dataset(fnames_out[ifile],"w")
    nc_out.createDimension(levname,len(lev_out))
    nc_out.createDimension(numname,len(OBS_number))
    nc_out.createVariable(levname,"float",[levname])
    nc_out.variables[levname].units="m"
    nc_out.variables[levname][:]=lev_out[:]
    nc_out.createVariable("T","float",[numname,levname])
    nc_out.createVariable("S","float",[numname,levname])
    nc_out.createVariable("time","float",[numname])
    nc_out.createVariable("lon","float",[numname])
    nc_out.createVariable("lat","float",[numname])
    WMO_number=np.asarray(WMO_number)
    nc_out.createVariable("WMO_number","str",[numname])
    nc_out.createVariable("obsnum","int",[numname])
    nc_out.createVariable("obsymnum","int",[numname])
    time_out_day=[(i-ref_dt).days+(i-ref_dt).seconds/(60.0*60.0*24.0) for i in time_out]
    nc_out.variables["lon"].long_name="longitude"
    nc_out.variables["lat"].long_name="latitude"
    nc_out.variables["time"].long_name="time"
    nc_out.variables["T"].long_name="Potential temperature"
    nc_out.variables["S"].long_name="Salinity"
    nc_out.variables["WMO_number"].long_name="WMO number"
    nc_out.variables["obsnum"].long_name="Observation number"
    nc_out.variables["obsymnum"].long_name="Observation YYYYMM"

    nc_out.variables["lon"].units="degrees_east"
    nc_out.variables["lat"].units="degrees_north"
    nc_out.variables[levname].units="m"
    nc_out.variables["time"].units=time_units
    nc_out.variables["T"].units="degrees celsius"
    nc_out.variables["S"].units="psu"

    nc_out.variables["lon"][:]=np.asarray(lon_out)
    nc_out.variables["lat"][:]=np.asarray(lat_out)
    nc_out.variables["time"][:]=np.asarray(time_out_day)
    nc_out.variables["obsnum"][:]=np.asarray(OBS_number)
    nc_out.variables["obsymnum"][:]=np.asarray(OBS_yyyymm)
    nc_out.variables["WMO_number"][:]=np.asarray(WMO_number)
    nc_out.variables["T"].long_name="Potential temperature"
    nc_out.variables["S"].long_name="Salinity"
    nc_out.variables["T"].missing_value=missing
    nc_out.variables["S"].missing_value=missing
    nc_out.variables["T"][:]=np.ones((len(OBS_number),len(lev_out)))*missing
    nc_out.variables["S"][:]=np.ones((len(OBS_number),len(lev_out)))*missing
    nc_out.system_name=system_name
    nc_out.exp_name=exp_name
    nc_out.data_type=type_name
    nc_out.close()
 
