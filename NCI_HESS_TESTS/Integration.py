import os
import sys
import numpy as np
import subprocess

#os.system("crest --help")
#subprocess.run(["crest","--help"])

n=int(input("Number of fundamental moieties: "))
print(n)
xyz_files = []
fundamental_moieties = []
charges = []
uhf = []
number_of_moieties = []
print("If .xyz files of the Fundamental Moieties are in this directory, enter their name. If not, enter the location + name of the files")
for i in range(1,n+1):
    xyz_files.append(input())
    print("label:")
    fundamental_moieties.append(input())
    print("charge:")
    charges.append(input())
    print("Multiplicity:")
    uhf.append(input())
print(fundamental_moieties)
print("Enter the composition of the precursor ion")
for i in range(1,n+1):
    print(fundamental_moieties[i-1],":")
    number_of_moieties.append(int(input()))
print("Parent non-covalent Ion at level 0 of fragmentation has following molecular entities : ")
for i in range(0,n):
   print(number_of_moieties[i],fundamental_moieties[i])
levels=0
parent_ion=[number_of_moieties,fundamental_moieties,levels]
print(parent_ion)
def FragmentationGraph(parent_ion):
    levels=0
    [number_of_moieties,fundamental_moieties,levels]=parent_ion
    daughter_ions=[]
    seen = set()
    for i in range(0,n):
        d_number_of_moieties=number_of_moieties[:]
        d_number_of_moieties[i]=d_number_of_moieties[i]-1
        daughter_ions.append([number_of_moieties,d_number_of_moieties,fundamental_moieties,levels+1])
        del(d_number_of_moieties)
    levels=levels+1

    max_levels=50
    for i in range(2,max_levels):
        for item in daughter_ions:
            if item[3]==i-1:
                for j in range(0,n):
                    d_number_of_moieties=item[1][:]
                    d_number_of_moieties[j]=d_number_of_moieties[j]-1
                    if d_number_of_moieties[j]>=0:
                        k=tuple(d_number_of_moieties)
                        if k not in seen:
                            seen.add(k)
                            daughter_ions.append([item[1][:],d_number_of_moieties,fundamental_moieties,i])
                    del(d_number_of_moieties)
    number_of_daughter_ions=0
    for item in daughter_ions:
        print(item)
        number_of_daughter_ions=number_of_daughter_ions+1
    print(number_of_daughter_ions)
FragmentationGraph(parent_ion)
number_of_moieties_str=[]
for item in number_of_moieties:
    number_of_moieties_str.append(str(item))
if os.path.exists(fundamental_moieties[1]):
    subprocess.run(["cp",xyz_files[1],fundamental_moieties[1]])
    subprocess.run(["cp",xyz_files[0],fundamental_moieties[1]])
else:
    subprocess.run(["mkdir",fundamental_moieties[1]])
    subprocess.run(["cp",xyz_files[0],fundamental_moieties[1]])
    subprocess.run(["cp",xyz_files[1],fundamental_moieties[1]])
os.chdir(fundamental_moieties[1])
subprocess.run(["crest",xyz_files[1],"--chrg",charges[1],"--uhf",uhf[1],"--qcg",xyz_files[0],"--nsolv",number_of_moieties_str[0],"--xtbiff","/home/software/xtbiff","--gfnff","--T","5","--nofix"])
#os.system("cd grow")
print("NCI + HESS (1) OR NCI_THEN_HESS (2)?")
nci_hess_decision=input()
if nci_hess_decision=="1":
    os.system("cp grow/cluster_optimized.xyz .")
    subprocess.run(["crest","cluster_optimized.xyz","--nci","--prop","hess","--T","5", "&&"],capture_output=True)
if nci_hess_decision=="2":
    os.system("cp grow/cluster_optimized.xyz .")
    subprocess.run(["crest","cluster_optimized.xyz","--nci","--T","5","&&"])
    subprocess.run(["crest","crest_best.xyz","--for","crest_conformers.xyz","--prop","hess","--T","5","&&"],capture_output=True)