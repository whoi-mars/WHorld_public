
#   OLD- NOT USED ANYMORE


import netCDF4 as nc
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import dive_profile
import matplotlib.pyplot as plt

entries = os.listdir('data/')
state0=np.array([])
state1=np.array([])
state2=np.array([])

# filename = 'tdr100516eg13.nc'
for filename in entries:
    print(filename)
    ncin = Dataset('data/' + filename, 'r', format='NETCDF')
    depth = ncin.variables['depth'][:] # meters, each time step=1sec
    depth_state=np.array(depth)
    depth_state[depth<9.9]=0 #todo change back
    depth_state[depth>9.9]=1
    depth_state[depth>=10]=2
    # plt.plot(-depth_state)
    # plt.show()

    last = 9999
    state = np.array(np.nan)
    count=0
    for k in depth_state:
        if k == last:
            count=count+1
            last = k
        else:
            writeout = count
            count=1
            last = k
            if writeout>10 :  #if whale is in a state for less than 10 sec, disregard
                print(writeout)
                state = last
                if state==0 and writeout<1800: # at surface for less than 30 min
                    state0 = np.append(state0, writeout)
                elif state==1:
                    state1 = np.append(state1, writeout)
                elif state == 2:
                    state2 = np.append(state2, writeout)
vec_0=state0
vec_1=state1
vec_2=state2

pickle.dump([vec_0,vec_1,vec_2], open("dp/vec012.p", "wb"))

dp=dive_profile.create_dive_profile(vec_0,vec_1,vec_2,30)

#vec_0,vec_1,vec_2, = pickle.load(open("vec012.p","rb"))

#print(c,d) ## To verify

# # HISTOGRAMS
fig1, ax1 = plt.subplots(3)
# np.histogram(vec_0)
# np.histogram(vec_0)
# np.histogram(vec_0)

ax1[0].hist(vec_0, bins='auto')
ax1[0].set_title('Lengths of vector 0')
ax1[0].set_xlabel('Length (s)')

ax1[1].hist(vec_1, bins='auto')
ax1[1].set_title('Lengths of vector 1')
ax1[1].set_xlabel('Length (s)')

ax1[2].hist(vec_2, bins='auto')
ax1[2].set_title('Lengths of vector 2')
ax1[2].set_xlabel('Length (s)')
plt.show()



# plt.figure(1)
# #plt.plot(speed,probs_average,linestyle='solid')
# plt.plot(depth_state)
# plt.plot(depth)
# plt.xlabel('Time [ sec]')
# plt.ylabel('depth_state')
# #plt.title('In-time probability of detectable_whales_xyz, #iter=%i'%(iter))
# plt.show()
#
#
# print(depth_state)

#
# for var in ncin.variables.values('time'):
#     print(var)
# prcp = ncin['time2'][:]
# a = ncin['time2']
# #for all netcdf files
# time = ncin.variables['time'][:]
# time2 = ncin.variables['time2'][:]
# print(depth)
# check netCDF file format

