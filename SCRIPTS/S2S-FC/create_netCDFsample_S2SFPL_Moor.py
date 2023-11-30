# Python script for generating netCDF sample for S2SF-PL Mooring
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../S2S-FC"
start_year=2003;start_month=2
end_year=2004;end_month=1
#end_year=2023;end_month=1
mem_start=1; mem_end=2
institution_name="JMA-MRI"
contact_name="yfujii@mri-jma.go.jp"
system_name="SAMPLE"
exp_names=["CNTL"]  # Name of experiments
version_name="0"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="S2SF-PL"
plat_name="Mooring"
plat_short="Moor"
time_interp="daily average value"
nskip=1

varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("T");vartypes.append("TLLL");varlong.append("Potential temperature with respect to 0m");varunits.append("Degree C")
varnames_out.append("S");vartypes.append("TLLL");varlong.append("Practical Salinity");varunits.append("psu")
varnames_out.append("U");vartypes.append("TLLL");varlong.append("Zonal Velocity");varunits.append("m/s")
varnames_out.append("V");vartypes.append("TLLL");varlong.append("Meridional Velocity");varunits.append("m/s")
varnames_out.append("SWHF");vartypes.append("TLL");varlong.append("Shortwave (solar) heat flux at the sea surface; positive downward");varunits.append("W/m^2")
varnames_out.append("NetHF");vartypes.append("TLL");varlong.append("Net heat flux at the sea surface; positive downward");varunits.append("W/m^2")
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
print(mname)
missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"
lead_times=[35,35,35,35,126,35,35,35,35,35,126,35]

lonname="longitude"
latname="latitude"
levname="depth"
timename="juld"
posname="npoint"

for iexp in range(0,len(exp_names)):
    fflag_tail="_"+system_name+"_"+exp_names[iexp]+".nc"
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
            dt_ini=dt.datetime(iy,im,1,0,0,0)
            initial_time=dt_ini.strftime('%Y-%m-%d %H:%M:%S utc')
            yyyymm=iy*100+im
            for mem in range(mem_start,mem_end+1):
                member_out=np.asarray([mem])
                mem_str="E"+'{:0>2d}'.format(mem)
                dir_name=dir_work+"/"+system_name+"/"+exp_names[iexp]+"/I"+str(yyyymm)+"/" + mem_str \
                        +'/'+group_name+'/'+plat_short
                os.makedirs(dir_name,exist_ok=True)
                fname_out=dir_name+"/"+group_name+"_"+plat_short \
                    +"_I"+str(yyyymm)+"_"+mem_str+fflag_tail

                time_out_day=[]
                lead_time_out=[]
                for lt in range(1,lead_times[im-1]+1):
                    lt_str='D'+'{:0>3d}'.format(lt)
                    lead_time_out.append(lt_str)
                    dt_tmp=dt_ini+dt.timedelta(days=lt-1)
                    time_out_day.append((dt_tmp-ref_dt).days)

                nc_out=ncdf.Dataset(fname_out,"w")
                nc_out.createDimension(levname,len(lev_out))
                nc_out.createDimension(timename,len(time_out_day))
                nc_out.createDimension(posname,len(lon_point))
                nc_out.createVariable(levname,"float32",[levname])
                nc_out.createVariable(timename,"double",[timename])
                nc_out.createVariable("lead_time","str",[timename])
                nc_out.createVariable("Mooring_name","str",[posname])
                nc_out.createVariable(lonname,"float32",[posname])
                nc_out.createVariable(latname,"float32",[posname])
                nc_out.variables[lonname].long_name="Longitude"
                nc_out.variables[lonname].units="degrees_east"
                nc_out.variables[lonname][:]=np.asarray(lon_point)
                nc_out.variables[latname].long_name="Latitude"
                nc_out.variables[latname].units="degrees_north"
                nc_out.variables[latname][:]=np.asarray(lat_point)
                nc_out.variables[levname].long_name="Depths"
                nc_out.variables[levname].units="m"
                nc_out.variables[levname][:]=np.asarray(lev_out)
                nc_out.variables[timename].long_name="Initial time of the valid day"
                nc_out.variables[timename].units=time_units
                nc_out.variables[timename][:]=np.asarray(time_out_day)
                nc_out.variables["lead_time"].long_name="Lead time index of the valid day"
                nc_out.variables["lead_time"][:]=np.asarray(lead_time_out)

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
                nc_out.member=mem_str
                nc_out.version=version_name
                nc_out.time_interp=time_interp
                nc_out.creation_date=creation_date

                nc_out.close()
            
