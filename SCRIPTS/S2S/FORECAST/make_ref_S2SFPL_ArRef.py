# Python script for generating netCDF sample for S2SF-PL Reference Argo
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
version_name="0"
dir_argo="../../../Argo_Info/" # Path to files with "ArRefYYYYMM"

# You don't need to edit following part
dt_now=dt.datetime.now(dt.timezone.utc)
creation_date=dt_now.strftime('%Y-%m-%d %H:%M:%S utc')
project_name="SynObs Flagship OSE"
group_name="S2SF-PL"
plat_name="Reference Argo"
plat_short="ArRef"
time_interp="daily average value"
obs_num_start=50000
nskip=1

missing=-9.99e7
ref_dt=dt.datetime(1950,1,1,0,0,0); time_units="Days since "+str(ref_dt)+" utc"
lev_out=[1.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 270.0, 300.0, 330.0, 360.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1350.0, 1500.0, 1750.0, 2000.0]
lead_times=[35,35,35,35,126,35,35,35,35,35,126,35]

lonname="longitude"
latname="latitude"
levname="depth"
timename="juld"
numname="numobs"


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
      dir_name=dir_work+"/"+system_name+"/I"+str(yyyymm)+"/" + mem_str \
            +'/'+group_name+'/'+plat_short
      os.makedirs(dir_name,exist_ok=True)
      fflag_tail="_"+system_name+".nc"
      fname_out=dir_name+"/"+group_name+"_"+plat_short \
          +"_I"+str(yyyymm)+"_"+mem_str+fflag_tail
      lon_out=[];lat_out=[];time_out=[]
      temp_out=[];salt_out=[]
      WMO_number=[];OBS_number=[];OBS_yyyymm=[]
      lead_time_out=[]
      iytt=iy
      imtt=im
      dt_tmp=dt_ini
      lt_file_days=1  
      iprof=0
      while lt_file_days < lead_times[im-1]+1:
        yyyymm2=dt_tmp.year*100+dt_tmp.month
        fname_in=dir_argo+plat_short+"/"+str(int(yyyymm2/100))+"/ArRef"+str(yyyymm2)
        f=open(fname_in,"r")
        lines=f.readlines()
        reach_end=False
        iline=0
        while reach_end == False:
            tmp=lines[iline]
            dt_obs=dt.datetime(int(tmp[0:4]),int(tmp[4:6]),int(tmp[6:8]),int(tmp[8:10]),int(tmp[10:12]),0)
            lt_obs=(dt_obs-dt_ini).days+1
            lat=float(tmp[12:17])/100
            lon=float(tmp[17:23])/100
            lon_out.append(lon)
            lat_out.append(lat)
            time_out.append(dt_tmp)
            lt_str='D'+'{:0>3d}'.format(lt_obs)
            lead_time_out.append(lt_str)
            wmo_tmp=tmp[31:38]
            WMO_number.append(wmo_tmp)
            OBS_number.append(obs_num_start+iprof)
            OBS_yyyymm.append(yyyymm2)
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
   
        imtt=imtt+1
        if (imtt>12):
          iytt=iytt+1
          imtt=1
        dt_tmp=dt.datetime(iytt,imtt,1,0,0,0)
        lt_file_days=(dt_tmp-dt_ini).days+1  

      time_out_day=[(i-ref_dt).days+(i-ref_dt).seconds/(60.0*60.0*24.0) for i in time_out]

      # Create netCDF file
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
      nc_out.createVariable("OBS_number","int",[numname])
      nc_out.createVariable("WMO_number","str",[numname])
      nc_out.createVariable("OBS_ym","int",[numname])

      nc_out.variables[lonname].long_name="Longitude"
      nc_out.variables[latname].long_name="Latitude"
      nc_out.variables[timename].long_name="Observation time"
      nc_out.variables['lead_time'].long_name="Lead time index of the valid day"
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
      nc_out.variables["lead_time"][:]=np.asarray(lead_time_out)
      nc_out.variables["OBS_number"][:]=np.asarray(OBS_number)
      nc_out.variables["OBS_ym"][:]=np.asarray(OBS_yyyymm)
      nc_out.variables["WMO_number"][:]=np.asarray(WMO_number)
      nc_out.variables["T"].missing_value=missing
      nc_out.variables["S"].missing_value=missing
      nc_out.variables["T"][:]=np.ones((len(OBS_number),len(lev_out)))*missing
      nc_out.variables["S"][:]=np.ones((len(OBS_number),len(lev_out)))*missing

      title_name=project_name+" "+group_name+" "+plat_name+" Data"
      nc_out.title=title_name
      nc_out.institution=institution_name
      nc_out.contact=contact_name
      nc_out.system=system_name
      nc_out.initial_time=initial_time
      nc_out.member=mem_str
      nc_out.version=version_name
      nc_out.time_interp=time_interp
      nc_out.creation_date=creation_date

      nc_out.close()

