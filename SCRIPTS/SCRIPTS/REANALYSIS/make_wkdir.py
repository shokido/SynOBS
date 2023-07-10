# Python script for preparing working directories
import os
dir_home="../../REANALYSIS/"

dir_names=[]
dir_names.append(dir_home+"OP_G1")
dir_names.append(dir_home+"OP_G2")
dir_names.append(dir_home+"OP_G2H")
dir_names.append(dir_home+"OP_G3Argo")
dir_names.append(dir_home+"OP_G3Mooring")

# Make working directories
for i in dir_names:
    if (os.path.exists(i)==False):
        os.makedirs(i)