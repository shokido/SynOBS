# Python script for generating netCDF file for S2S-PL ArAsm
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../../S2S-AN"
dt_start=dt.datetime(2003,1,1,0,0,0) # Start date of output
dt_end=dt.datetime(2003,1,31,0,0,0)  # End date of output (for an initial test...terminate at 31/1/2003)
#dt_end=dt.datetime(2022,12,31,0,0,0)  # End date of output
institution_name="JMA/MRI"
contact_name="yfujii@mri-jma.go.jp"
system_name="OBSDATA" # Name of your system
version_name="0"
dir_argo="../../../Argo_Info/" # Path to files with "ArRefYYYYMM"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="S2S-PL"
plat_name="Reference Argo"
plat_short="ArRef"
time_interp="daily average value"
obs_num_start=50000

missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"
lev_out=[1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 270.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1350.0, 1500.0, 1750.0, 2000.0]

lonname="longitude"
latname="latitude"
levname="depth"
timename="juld"
numname="numobs"


start_year=dt_start.year;start_month=dt_start.month
end_year=dt_end.year;end_month=dt_end.month
fnames_Argo=[]
fnames_out=[]
dir_out=dir_work+"/"+system_name+"/"+group_name+"/"+plat_short
os.makedirs(dir_out,exist_ok=True)
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
        yyyymm=iy*100+im
        dir_out=dir_work+"/"+system_name+"/"+group_name+"/"+plat_short
        fflag_tail="_"+system_name+".nc"
        fname_out=dir_out+"/"+group_name+"_"+plat_short+"_" \
                   +str(yyyymm)+fflag_tail
        fnames_out.append(fname_out)
        fnames_Argo.append(dir_argo+plat_short+"/"+str(iy)+"/ArRef"+str(yyyymm))

nfile=len(fnames_Argo)

for ifile in range(0,nfile):
    f=open(fnames_Argo[ifile],"r")
    lines=f.readlines()

    lon_out=[];lat_out=[];time_out=[]
    temp_out=[]
    salt_out=[]
    WMO_number=[];OBS_number=[];OBS_yyyymm=[]
    reach_end=False
    iline=0;iprof=0
    while reach_end == False:
        tmp=lines[iline]
        dt_tmp=dt.datetime(int(tmp[0:4]),int(tmp[4:6]),int(tmp[6:8]),int(tmp[8:10]),int(tmp[10:12]),0)
        lat=float(tmp[12:17])/100
        lon=float(tmp[17:23])/100
        lon_out.append(lon)
        lat_out.append(lat)
        time_out.append(dt_tmp)
        wmo_tmp=tmp[31:38]
        WMO_number.append(wmo_tmp)
        OBS_number.append(obs_num_start+iprof)
        OBS_yyyymm.append(dt_tmp.year*100+dt_tmp.month)
        isS=tmp[38]
        varflag=tmp[39]
        tmp_T=tmp[40:]
        nz=int(len(tmp_T)/5)
        temp_tmp=np.ones((len(lev_out)))*missing
        salt_tmp=np.ones((len(lev_out)))*missing
        for iz in range(0,nz):
            iz1=iz*5
            iz2=iz*5+5
            val=float(tmp_T[iz1:iz2])/1000
            if (val ==99.999):
                val=missing
            temp_tmp[iz]=val
        if (isS=="2"):
            iline+=1
            tmp=lines[iline]
            varflag=tmp[39]
            assert varflag == "S"
            tmp_S=tmp[40:]
            nz=int(len(tmp_S)/5)
            for iz in range(0,nz):
                iz1=iz*5
                iz2=iz*5+5
                val=float(tmp_S[iz1:iz2])/1000
                if (val ==99.999):
                    val=missing
                salt_tmp[iz]=val
        else:
            for iz in range(0,nz):
                salt_tmp[iz]=missing
        iline+=1
        iprof+=1
        temp_out.append(temp_tmp)
        salt_out.append(salt_tmp)
        if (iline==len(lines)):
            reach_end=True
    # Create netCDF file
    nprof=len(lon_out)
    nc_out=ncdf.Dataset(fnames_out[ifile],"w")
    nc_out.createDimension(levname,len(lev_out))
    nc_out.createDimension(numname,len(OBS_number))
    nc_out.createVariable(levname,"float32",[levname])
    nc_out.variables[levname].long_name="Depths"
    nc_out.variables[levname].units="m"
    nc_out.variables[levname][:]=lev_out[:]
    nc_out.createVariable("T","float32",[numname,levname])
    nc_out.createVariable("S","float32",[numname,levname])
    nc_out.createVariable(timename,"double",[numname])
    nc_out.createVariable(lonname,"float32",[numname])
    nc_out.createVariable(latname,"float32",[numname])
    WMO_number=np.asarray(WMO_number)
    nc_out.createVariable("WMO_number","str",[numname])
    nc_out.createVariable("OBS_number","int",[numname])
    nc_out.createVariable("OBS_ym","int",[numname])
    time_out_day=[(i-ref_dt).days+(i-ref_dt).seconds/(60.0*60.0*24.0) for i in time_out]
    nc_out.variables[lonname].long_name="Longitude"
    nc_out.variables[latname].long_name="latitude"
    nc_out.variables[timename].long_name="Observation time"
    nc_out.variables["T"].long_name="Potential temperature"
    nc_out.variables["S"].long_name="Salinity"
    nc_out.variables["WMO_number"].long_name="WMO number"
    nc_out.variables["OBS_number"].long_name="Observation number"
    nc_out.variables["OBS_ym"].long_name="Observation YYYYMM"

    nc_out.variables[lonname].units="degrees_east"
    nc_out.variables[latname].units="degrees_north"
    nc_out.variables[timename].units=time_units
    nc_out.variables["T"].units="degrees celsius"
    nc_out.variables["S"].units="psu"

    nc_out.variables[lonname][:]=np.asarray(lon_out)
    nc_out.variables[latname][:]=np.asarray(lat_out)
    nc_out.variables[timename][:]=np.asarray(time_out_day)
    nc_out.variables["OBS_number"][:]=np.asarray(OBS_number)
    nc_out.variables["OBS_ym"][:]=np.asarray(OBS_yyyymm)
    nc_out.variables["WMO_number"][:]=np.asarray(WMO_number)
    nc_out.variables["T"].missing_value=missing
    nc_out.variables["S"].missing_value=missing
    for iprof in range(0,nprof):
        nc_out.variables["T"][iprof,:]=temp_out[iprof]
        nc_out.variables["S"][iprof,:]=salt_out[iprof]
    #         nc_out.variables["T"][:]=np.ones((len(OBS_number),len(lev_out)))*missing
    # nc_out.variables["S"][:]=np.ones((len(OBS_number),len(lev_out)))*missing

    title_name=project_name+" "+group_name+" "+plat_name+" Data"
    nc_out.title=title_name
    nc_out.institution=institution_name
    nc_out.contact=contact_name
    nc_out.system=system_name
    nc_out.version=version_name
    nc_out.time_interp=time_interp
    nc_out.creation_date=creation_date

    nc_out.close()

