# Python script for preparing working directories
import os
dir_home="../../PREDICTION/"

dir_names=[]
dir_names.append(dir_home+"OPF_G1")
dir_names.append(dir_home+"OPF_G2")
dir_names.append(dir_home+"OPF_G2H")
dir_names.append(dir_home+"OPF_G3Argo")
dir_names.append(dir_home+"OPF_G3Mooring")

# Make working directories
for i in dir_names:
    if (os.path.exists(i)==False):
        os.makedirs(i)
