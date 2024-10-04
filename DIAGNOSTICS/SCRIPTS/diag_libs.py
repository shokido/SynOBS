"""
  Sea water state functions 
		based on UNESCO algorithms
		The code is based on  Phil Morgan 1993, CSIRO
  Matlab version
"""
import numpy as np
import sys

def sw_press(zz,LAT):
  """
  REFERENCE: Saunders, P.M., 1981
  "Practical conversion of Pressure to Depth"
  JPO, 11, 573-574

  The code is similar to the sw_pres.m developed by
  Phil Morgan 1993, CSIRO
  """

#  if np.isscalar(zz):
#    lat0 = LAT
#  elif isinstance(zz,np.ndarray):
#    if np.dim(zz)==1:
#      lat0=LAT
#    else:
#      nrws = zz.shape[0]
#      nclm = zz.shape[1]
#      
#    for ii in range(nclm):
#      lat0 = LAT[:,ii]
  zz=np.abs(zz)  
##      breakpoint()
# Check shapes 

  if isinstance(zz,np.ndarray):
    if not isinstance(LAT,np.ndarray):
      print('ERROR: Depth Z is array and LAT is not array')
      sys.exit()
    else:
      zdim = zz.ndim
      ldim = LAT.ndim
      if zdim != ldim:
        print('ERROR: Z dim={0}, Lat dim={1}, should be equal'.format(zdim,ldim))
        sys.exit()

 
  deg2rad = np.pi/180.
  X    = np.sin(np.abs(LAT)*deg2rad)
  C1   = 5.92e-3+X**2*5.25e-3
  pres_db = ((1.-C1)-np.sqrt(((1.-C1)**2)-(8.84e-6*zz)))/(4.42e-6) # dbar
  pres_pa = pres_db*1.e4  # Pa


  return pres_db, pres_pa

def adiab_Tgrad(S,T,P):
  """
    Calculates adiabatic T gradient as per UNESCO 1983
    all input fields must have same dim

    Possible types: scalar (float) or 2D numpy arrays
    
    S  = salinity, psu PSS-78
    T  = temperature, C dgr ITS-90
    P  = pressure, db

    Based on P. Morgan code
  """
  
# Check dim:
  if isinstance(S,np.ndarray):
#    print('type S={0}'.format(type(S))
    ndim = S.ndim
    jS  =  S.shape[0]
    jT = T.shape[0]
    jP = P.shape[0]

    iS = 0
    iT = 0
    iP = 0
    if ndim==2:
      iS = S.shape[1]
      iT = T.shape[1]
      iP = P.shape[1]

    if jS != jT or jS != jP or iS != iP or iS != iT:
      print('adiab_Tgrad: ERROR dimensions of T,S,P do not match')
      print('{0}x{1} {2}x{3} {4}x{5}'.format(jS,iS,jT,iT,jP,iP))
      sys.exit()

  T68 = 1.00024*T

  a0 =  3.5803e-5
  a1 =  8.5258e-6
  a2 = -6.836e-8
  a3 =  6.6228e-10

  b0 =  1.8932e-6
  b1 = -4.2393e-8
  
  c0 =  1.8741e-8
  c1 = -6.7795e-10
  c2 =  8.733e-12
  c3 = -5.4481e-14

  d0 = -1.1351e-10
  d1 =  2.7759e-12

  e0 = -4.6206e-13
  e1 =  1.8676e-14
  e2 = -2.1687e-16

  adtg =   a0 + (a1 + (a2 + a3*T68)*T68)*T68 \
         + (b0 + b1*T68)*(S-35.) \
         + ((c0 + (c1 + (c2 + c3*T68)*T68)*T68) \
         + (d0 + d1*T68)*(S-35.))*P \
         + (e0 + (e1 + e2*T68)*T68)*P*P

  return adtg


#
def sw_ptmp(S,T,P1,Pref):
  """
    Potential T at reference pressure Pref adiabatically brought
    from Pressure=P1
    Based on UNESCO 1983 report - Phil Morgan Matlab code
    all variables have same dimensions (e.g. 2D arrays)
    S = salinity psu PSS-78
    T = temperature C deg ITS-90
    P1 = pressure dbar
    Pref = pressure reference dbar
  """

  if np.min(Pref)<0. or np.min(P1)<0:
    print('ERROR: Pressure must be >0 min Pref={0} P1={1}'.\
          format(np.min(Pref),np.min(P1)))
    sys.exit()

# theta 1
  del_P   = Pref - P1
  adtg    = adiab_Tgrad(S,T,P1)
  del_th  = del_P*adtg
  th      = T*1.00024 + 0.5*del_th
  q       = del_th

# theta 2
  adtg = adiab_Tgrad(S,th/1.00024,P1+0.5*del_P)
  del_th = del_P*adtg
  th     = th + (1.-1./np.sqrt(2.))*(del_th-q)
  q      = (2. - np.sqrt(2.))*del_th + (-2.+3./np.sqrt(2.))*q

# theta 3
  adtg   = adiab_Tgrad(S,th/1.00024,P1+0.5*del_P)
  del_th = del_P*adtg
  th     = th + (1.+1./np.sqrt(2.))*(del_th-q)
  q      = (2.+np.sqrt(2.))*del_th + (-2.-3./np.sqrt(2.))*q

# theta 4
  adtg   = adiab_Tgrad(S,th/1.00024,P1+del_P)
  del_th = del_P*adtg
  ptmp   = (th + (del_th - 2.*q)/6.)/1.00024

  return ptmp

#
#
def sw_smow(T):
  """
    Density of standard mean ocean water (pure water)
    UNESCO EOS 1980    

    Input T C deg ITS-90

    Output rho_S0 - kg/m3
  """
  a0 =  999.842594
  a1 =  6.793952e-2
  a2 = -9.095290e-3
  a3 =  1.001685e-4
  a4 = -1.120083e-6
  a5 =  6.536332e-9

  T68 = T*1.00024
  rho_S0 = a0 + (a1 + (a2 + (a3 + (a4 + a5*T68)*T68)*T68)*T68)*T68

  return rho_S0



def sw_dens0(S,T):
  """
    Sea water density at pressure=0, i.e. atmospheric pressure
    UNESCO 1983 (EOS 1980) polynomial

    S = salinity psu PSS-78
    T = temp. C deg ITS-90

    output: 
      rhoP0 kg/m3
    code is based on Phil Morgan's Matlab code

  """
  T68 = T*1.00024

# UNESCO 1983 eqn(13) p17
  b0 =  8.24493e-1
  b1 = -4.0899e-3
  b2 =  7.6438e-5
  b3 = -8.2467e-7
  b4 =  5.3875e-9

  c0 = -5.72466e-3
  c1 =  1.0227e-4
  c2 = -1.6546e-6

  d0 =  4.8314e-4

  rho_P0 = sw_smow(T) + (b0 + (b1 + (b2 + (b3 + b4*T68)*T68)*T68)*T68)*S \
                    + (c0 + (c1 + c2*T68)*T68)*S*np.sqrt(S) + d0*S**2

  return rho_P0


def sw_seck(S,T,P):
  """
    Secant bulk modulus (K) of sea water using equation of state 1980
    UNESCO polynomial

    S = salinity PSS-78
    T = temp  ITS-90
    P = pressure, db

    output
    K = Secant bulk modulus, bars
  """

#--------------------------------------------------------------------
#
# COMPUTE COMPRESSION TERMS
#
#--------------------------------------------------------------------

  P = P/10.  #convert from db to atmospheric pressure units
  T68 = T * 1.00024

# Pure water terms of the secant bulk modulus at atmos pressure.
# UNESCO eqn 19 p 18

  h3 = -5.77905E-7
  h2 = +1.16092E-4
  h1 = +1.43713E-3
  h0 = +3.239908   #[-0.1194975];

  AW  = h0 + (h1 + (h2 + h3*T68)*T68)*T68

  k2 =  5.2787E-8
  k1 = -6.12293E-6
  k0 =  8.50935E-5   #[+3.47718E-5];

  BW  = k0 + (k1 + k2*T68)*T68

  e4 = -5.155288E-5
  e3 =  1.360477E-2
  e2 = -2.327105
  e1 =  148.4206
  e0 =  19652.21    #[-1930.06];

  KW  = e0 + (e1 + (e2 + (e3 + e4*T68)*T68)*T68)*T68   #eqn 19

#--------------------------------------------------------------------
#
# SEA WATER TERMS OF SECANT BULK MODULUS AT ATMOS PRESSURE.
#
#--------------------------------------------------------------------

  j0 = 1.91075E-4 

  i2 = -1.6078E-6
  i1 = -1.0981E-5
  i0 =  2.2838E-3

  SR = np.sqrt(S)

  A  = AW + (i0 + (i1 + i2*T68)*T68 + j0*SR)*S

  m2 =  9.1697E-10
  m1 = +2.0816E-8
  m0 = -9.9348E-7

  B = BW + (m0 + (m1 + m2*T68)*T68)*S   # eqn 18

  f3 =  -6.1670E-5
  f2 =  +1.09987E-2
  f1 =  -0.603459
  f0 = +54.6746

  g2 = -5.3009E-4
  g1 = +1.6483E-2
  g0 = +7.944E-2

  K0 = KW + (f0 + (f1 + (f2 + f3*T68)*T68)*T68 \
        +   (g0 + (g1 + g2*T68)*T68)*SR)*S      # eqn 16
  K = K0 + (A + B*P)*P  # eqn 15

  return K


# Calculate sea water density at reference pressure 
def sw_dens(S,T,P):
  """
    Computes seawater density using UNESCO 1983 (EOS 80) polynomial

    All input fields must have same dimensions (or scalar)
    S = salinity PSS-78
    T = temp C deg, ITS-90
    P = pressure (>0 !) db

    output density rho kg/m3
  """

  rhoP0 = sw_dens0(S,T)
  K     = sw_seck(S,T,P)
  P     = P/10.   # db --> bar
  rho   = rhoP0/(1.-P/K)

  return rho

# Vertical interpolation
def pcws_lagr1(Xp,Yp,xx):
  """
   Piecewise linear Lagr. Polynomial degree 1
   Xp is assumed in Ascending Order
  """
  if Xp[1] < Xp[0]:
#    raise Exception('Xp should be increasing')
#    print('Xp is not in ascending order, flipping ...')
    Xp = np.flip(Xp)
    Yp = np.flip(Yp)

 # Find interval that contains point xx
  dmm = abs(Xp-xx)
  if (Xp[0]>=xx):
      i1=0
      i2=1  
  elif (Xp[-1]<=xx):
      i1=len(Xp)-2
      i2=len(Xp)-1
  else:
    imin = np.argmin(dmm)
    if Xp[imin] < xx :
      i1 = imin
      i2 = i1+1
    elif Xp[imin] == xx:  # node point, to avoid left/right boundary i-1/i+1 problem
      i1 = max([0,imin-1])
      i2 = i1+1
    else:
      i1 = imin-1
      i2 = imin

#  # Check dim if i1/i2 >/< max/min size Xp
#   if i1 < 0 or i2 > Xp.shape[0]:
#     print('ERROR: i1 {0} or i2 {1} is out of bound'.format(i1,i2))
#     sys.exit(1)

  Pn = Yp[i1]*(xx-Xp[i2])/(Xp[i1]-Xp[i2]) + \
       Yp[i2]*(xx-Xp[i1])/(Xp[i2]-Xp[i1])

  return Pn
def pcws_lagr1_multi(Xp,Yp,xs):
  res=[pcws_lagr1(Xp, Yp, i) for i in  xs]
  res=np.asarray(res)
  return(res)

def get_valid(x,y):
    ind_valid=np.where(np.isnan(y)==False)[0]
    x_valid=np.copy(x[ind_valid])
    y_valid=np.copy(y[ind_valid])
    return(x_valid,y_valid)

def cal_vint(Xp,Yp,x1,x2,ext_left=True,ext_right=False):
  if Xp[1] < Xp[0]:
    Xp = np.flip(Xp)
    Yp = np.flip(Yp)
  Xp_valid,Yp_valid=get_valid(Xp,Yp) # Remove nan values  
  if (len(Xp_valid)==0):
     return(np.nan)  
  xmin=Xp_valid[0];xmax=Xp_valid[-1] # Assume it is in ascending order
  if (x1 < xmin and ext_left==False):
     return(np.nan)
  else:
     x1_e=x1
  if (x2 > xmax and ext_right==False):
     return(np.nan)
  else:
     x2_e=x2
  # Obtain y1_e
  x_ref=np.asarray((x1_e))
  if (len(Xp_valid)==1):
     y1_e=Yp_valid[0]
  else:
     y1_e=pcws_lagr1(Xp_valid,Yp_valid,x1_e)
  y_ref=np.asarray((y1_e))
  x_ind=np.where((Xp_valid> x1_e) & (Xp_valid < x2_e))[0]
  if (len(x_ind)>0):
    x_vals=np.asarray([Xp_valid[i] for i in x_ind])
    y_vals=np.asarray([Yp_valid[i] for i in x_ind])
    x_ref=np.append(x_ref,x_vals)
    y_ref=np.append(y_ref,y_vals)

  x_ref=np.append(x_ref,x2_e)
  if (len(Xp_valid)==1):
     y2_e=Yp_valid[0]
  else:
     y2_e=pcws_lagr1(Xp_valid,Yp_valid,x2_e)
  y_ref=np.append(y_ref,y2_e)
  res=np.trapz(y_ref,x_ref)
  return(res)
def find_isothern(vars, depths, thres_var):
    # Find index where temperature crosses the isotherm
    # Note: depths should be increasing with index
    idx = np.where(np.diff(np.sign(vars - thres_var)))[0]
    if (vars[0]<thres_var):
        return np.nan
    if idx.size == 0:
        return np.nan  # return NaN if no isotherm found

    # For simplicity, we take the first crossing
    idx = idx[0]
    # Perform linear interpolation between the two depths
    x1, x2 = vars[idx], vars[idx + 1]
    y1, y2 = depths[idx], depths[idx + 1]

    var_depth = y1 + (y2 - y1) * (thres_var - x1) / (x2 - x1)
    return var_depth

def find_ild(temp, depths, thres_temp):
#    dens=sw_dens(salt,temp,depths)
    thres_var=temp[0]-thres_temp
    # Find index where temperature crosses the isotherm
    # Note: depths should be increasing with index
    idx = np.where(np.diff(np.sign(temp - thres_var)))[0]

    if idx.size == 0:
        return np.nan  # return NaN if no isotherm found

    # For simplicity, we take the first crossing
    idx = idx[0]
    # Perform linear interpolation between the two depths
    x1, x2 = temp[idx], temp[idx + 1]
    y1, y2 = depths[idx], depths[idx + 1]

    var_depth = y1 + (y2 - y1) * (thres_var - x1) / (x2 - x1)
    return var_depth

def find_mld_dens(temp,salt, depths, thres_dens):
#    dens=sw_dens(salt,temp,depths)
    dens=sw_dens(salt,temp,0)
    thres_var=dens[0]+thres_dens
    # Find index where temperature crosses the isotherm
    # Note: depths should be increasing with index
    idx = np.where(np.diff(np.sign(dens - thres_var)))[0]

    if idx.size == 0:
        return np.nan  # return NaN if no isotherm found

    # For simplicity, we take the first crossing
    idx = idx[0]
    # Perform linear interpolation between the two depths
    x1, x2 = dens[idx], dens[idx + 1]
    y1, y2 = depths[idx], depths[idx + 1]

    var_depth = y1 + (y2 - y1) * (thres_var - x1) / (x2 - x1)
#    return thres_var
    return var_depth

def find_tchp(temp,salt, depths):
    thres_temp=26.0
    # Find index where temperature crosses the isotherm
    # Note: depths should be increasing with index
    if (temp[0]<thres_temp):
        return np.nan

    idx = np.where(np.diff(np.sign(temp - thres_temp)))[0]

    if idx.size == 0:
        return np.nan  # return NaN if no isotherm found

    # For simplicity, we take the first crossing
    idx = idx[0]
    # Perform linear interpolation between the two depths
    x1, x2 = temp[idx], temp[idx + 1]
    y1, y2 = depths[idx], depths[idx + 1]
    var_depth = y1 + (y2 - y1) * (thres_temp - x1) / (x2 - x1)
    if (np.isnan(var_depth)==False):
      dens=sw_dens(salt,temp,0)
      CP=3.985e3
      tchp=cal_vint(depths,dens*CP*(temp-thres_temp),0,var_depth)
      return tchp
    else:
      return(np.nan)

