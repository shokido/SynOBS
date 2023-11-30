# Python script for generating netCDF sample for S2SF-G1DA
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
group_name="S2SF-DA"
time_interp="daily average fields"
interval=1

varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("OLR");vartypes.append("TLL");varlong.append("Outgoing longwave ratiation at the top of the atmosphere");varunits.append("W/m^2")
varnames_out.append("U200");vartypes.append("TLL");varlong.append("Zonl wind speed at 200 hPa");varunits.append("m/s")
varnames_out.append("U850");vartypes.append("TLL");varlong.append("Zonl wind speed at 850 hPa");varunits.append("m/s")
nvar=len(varnames_out)

lon_out=np.arange(0,360,1.0)
lat_out=np.arange(-90,90.25,1.0)
missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"
lead_times=[35,35,35,35,35,35,35,35,35,35,35,35]

lonname="longitude"
latname="latitude"
timename="juld"

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
        for ivar in range(0,nvar):
          for lt in range(1,lead_times[im-1]+1):
            lt_str='D'+'{:0>2d}'.format(lt)
            dt_tmp=dt_ini+dt.timedelta(days=(lt-1)*interval)
            time_out=np.asarray([(dt_tmp-ref_dt).days])
            dir_name=dir_work+"/"+system_name+"/"+exp_names[iexp]+"/I"+str(yyyymm)+"/" + mem_str \
              +'/'+group_name+"/"+varnames_out[ivar]
            os.makedirs(dir_name,exist_ok=True)
            fname_out=dir_name+"/"+group_name+"_"+varnames_out[ivar] \
              +"_I"+str(yyyymm)+"_"+mem_str+'_'+lt_str+fflag_tail
            lead_time_out=np.asarray([lt_str])

            # Create netCDF file
            nc_out=ncdf.Dataset(fname_out,"w")
            nc_out.createDimension(lonname,len(lon_out))
            nc_out.createDimension(latname,len(lat_out))
            nc_out.createDimension(timename,len(time_out))
            nc_out.createVariable(lonname,"float32",[lonname])
            nc_out.createVariable(latname,"float32",[latname])
            nc_out.createVariable(timename,"double",[timename])
            nc_out.createVariable('lead_time',"str",[timename])
            nc_out[lonname][:]=lon_out[:]
            nc_out[lonname].long_name="Longitude"
            nc_out[lonname].units="degrees_east"
            nc_out[latname][:]=lat_out[:]
            nc_out[latname].long_name="Latitude"
            nc_out[latname].units="degrees_north"
            nc_out[timename][:]=time_out[:]
            nc_out[timename].long_name="Initial time of the valid day"
            nc_out[timename].units=time_units
            nc_out["lead_time"][:]=lead_time_out[:]
            nc_out["lead_time"].long_name="Lead time index of the valid day"

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
            nc_out.member=mem_str
            nc_out.version=version_name
            nc_out.time_interp=time_interp
            nc_out.creation_date=creation_date
            nc_out.close()

