# Python script for generating netCDF sample for S2SF-G1MA
import netCDF4 as ncdf
import datetime as dt
import numpy as np
import os

dir_work="../../../S2S-FC"
start_year=2003;start_month=2
end_year=2004;end_month=1
#end_year=2023;end_month=1
mem_start=1; mem_end=2
institution_name="JMA-MRI"
contact_name="yfujii@mri-jma.go.jp"
system_name="SAMPLE"
exp_name="CNTL"
version_name="0"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="S2SF-G1MA"
time_interp="monthly average fields"
fflag_tail="_"+system_name+"_"+exp_name+".nc"

varnames_out=[];vartypes=[];varunits=[];varlong=[]
varnames_out.append("T2m");vartypes.append("TLL");varlong.append("Air Temperature at 2m high");varunits.append("degree C")
varnames_out.append("U10m");vartypes.append("TLL");varlong.append("Zonal wind speed at 10m high");varunits.append("m/s")
varnames_out.append("V10m");vartypes.append("TLL");varlong.append("Meridional wind speed at 10m high");varunits.append("m/s")
varnames_out.append("Tatm");vartypes.append("TLLL");varlong.append("Air Temperatureat pressure levels");varunits.append("degree C")
varnames_out.append("Uatm");vartypes.append("TLLL");varlong.append("Zonal wind speed at pressure levels");varunits.append("m/s")
varnames_out.append("Vatm");vartypes.append("TLLL");varlong.append("Meridional wind speed at pressure levels");varunits.append("m/s")
varnames_out.append("Qatm");vartypes.append("TLLL");varlong.append("Specific humidity at pressure levels");varunits.append("kg/kg")
varnames_out.append("MSLP");vartypes.append("TLL");varlong.append("Mean Sea lvel pressure");varunits.append("Pa")
varnames_out.append("Precip");vartypes.append("TLL");varlong.append("Total Precipitation accumulatd for 6 hours");varunits.append("kg/m^2")
varnames_out.append("TCC");vartypes.append("TLL");varlong.append("Total cloud cover");varunits.append("%")
varnames_out.append("OLR");vartypes.append("TLL");varlong.append("Outgoing longwave ratiation at the top of the atmosphere");varunits.append("W/m^2")
varnames_out.append("Taux");vartypes.append("TLL");varlong.append("Zonal wind stress at the surface");varunits.append("N/m^2")
varnames_out.append("Tauy");vartypes.append("TLL");varlong.append("Meridional wind stress at the surface");varunits.append("N/m^2")
varnames_out.append("SWHF");vartypes.append("TLL");varlong.append("Shortwave (solar) heat flux at the sea surface; positive downward");varunits.append("W/m^2")
varnames_out.append("LWHF");vartypes.append("TLL");varlong.append("Longwave heat flux at the sea surface; positive downward");varunits.append("W/m^2")
varnames_out.append("SNHF");vartypes.append("TLL");varlong.append("Sensible heat flux at the sea surface; positive downward");varunits.append("W/m^2")
varnames_out.append("LAHF");vartypes.append("TLL");varlong.append("Latent heat flux at the sea surfac; positive downwarde");varunits.append("W/m^2")
nvar=len(varnames_out)
lev_out=[100000,92500,85000,70000,50000,30000,20000,10000,5000,1000]

lon_out=np.arange(0,360,1.0)
lat_out=np.arange(-90,90.25,1.0)
missing=-9.99E7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"
lead_times=[1,1,1,1,4,1,1,1,1,1,4,1]

lonname="longitude"
latname="latitude"
timename="juld"
levname="pressure_level"

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
        lt=1
        iyt=iy
        imt=im
        while lt<lead_times[im-1]+1:
          lt_str='M'+'{:0>2d}'.format(lt)
          dt_tmp=dt.datetime(iyt,imt,1,0,0,0)
          iyn=iyt
          imn=imt+1
          if (imn>12):
            iyn=iyn+1
            imn=1
          dt_end=dt.datetime(iyn,imn,1,0,0,0)
          time_out=np.asarray([(dt_tmp-ref_dt).days])
          dir_name=dir_work+"/"+exp_name+"/I"+str(yyyymm)+"/" + mem_str \
             +'/'+group_name+"/"+varnames_out[ivar]
          os.makedirs(dir_name,exist_ok=True)
          fname_out=dir_name+"/"+group_name+"_"+varnames_out[ivar] \
            +"_I"+str(yyyymm)+"_"+mem_str+'_'+lt_str+fflag_tail
          leadtime_str='D'+'{:0>3d}'.format((dt_tmp-dt_ini).days+1)
          leadtime_end='D'+'{:0>3d}'.format((dt_end-dt_ini).days)
          lead_time_out=np.asarray([lt_str+' ('+leadtime_str+'-' \
                      +leadtime_end+')'])

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
          nc_out[timename].long_name="Initial time of the valid month"
          nc_out[timename].units=time_units
          nc_out["lead_time"][:]=lead_time_out[:]
          nc_out["lead_time"].long_name="Lead time indices of the valid month and the first and last days of the month"

          if (vartypes[ivar]=="TLLL"):
             nc_out.createDimension(levname,len(lev_out))
             nc_out.createVariable(levname,"float32",[levname])
             nc_out[levname][:]=lev_out
             nc_out[levname].units="Pa"
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
          nc_out.exp_name=exp_name
          nc_out.initial_time=initial_time
          nc_out.member=mem_str
          nc_out.version=version_name
          nc_out.time_interp=time_interp
          nc_out.creation_date=creation_date
          nc_out.close()

          lt=lt+1
          imt=imt+1
          if (imt>12):
            iyt=iyt+1
            imt=1

