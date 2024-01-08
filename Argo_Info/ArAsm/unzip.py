import subprocess

for iy in range(2003,2023):
    command="gunzip argoasm"+str(iy)+".tar.gz"
    subprocess.call(command.split())
    command="tar -xvzf argoasm"+str(iy)+".tar"
    subprocess.call(command.split())