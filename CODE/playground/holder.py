'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script plots cross-result plots

Note: DOES not WORK
'''

#STEP 2

## WHAT THIS CODE INCLUDES: FUNCTIONS TO :
# DO THE INITIAL TRIAGE: GOOD/BAD FILES, +ADJUST START/END POINTS on good ones ==> pickle
# ADD SHALLOW/DEEP CLASSIFICATION ==> pickle
# READ/STORE IN DICT GOOD SEGMENTS OF REAL DEPTH
# CREATE STATE DP FROM REAL DP
# OBTAIN VEC 0/1/2/3 OF LENGTH
# OBTAIN NUMBER OF 2>1 AND 2>3 TRANSITIONS
# PLOTS REAL DEPTH/STATE DEPTH/VEC0123 HISTO

import pandas as pd
import os
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pickle



def mark_bad_good_files(directory):
    import os
    import numpy as np
    from netCDF4 import Dataset
    import matplotlib.pyplot as plt
    import pickle

    entries = os.listdir(directory)

    repertoire = {}

    for filename in entries:
        ncin = Dataset('/DATA/NARWdive_profiles_data/' + filename, 'r', format='NETCDF')
        depth = (-1) * ncin.variables['depth'][:]  # meters, each time step=1sec
        plt.plot(depth)
        plt.title(filename)
        plt.ylim(-200, 0)
        plt.grid()

        list1 = plt.ginput(n=3, show_clicks=True, mouse_add=1, mouse_pop=3)
        plt.close()
        list1 = np.asarray(list1)[:, 0]  # x axis or seconds to keep
        list1 = np.append(filename, list1)  # list
        repertoire[filename] = list1

    pickle.dump(repertoire, open("DATA/repertoires/triage_repertoire3", "wb"))
    print('Pickle file repertoires/triage_repertoire3 created!')

def trimmed_selectedfiles(repertoire_to_improve,name_pickle_file):
    #STEP 2: after raw data triage:

    # KEEP ONLY FILES W/ POSITIVE THIRD CLICK
    # ADJUST START/END POINTS OF EACH FILE

    path="/DATA/repertoires/"
    original_repert = pd.read_pickle(path+repertoire_to_improve)
    entries = os.listdir('/DATA/NARWdive_profiles_data/')
    new_repert={}

    #CREATE NEW REPERTOIRE FROM TRIAGE PROCESS
    i=0
    for filename in entries:
        if float(original_repert[filename][3])>0: #keep only files where third click was positive (by design)
            new_repert[i]=original_repert[filename][0:-1] #remove third click
            i=i+1

    #IMPROVE START/END POINTS FOR ALL GOOD FILES
    for i in range(len(new_repert)):
        # SET START POINT
        if float(new_repert[i][1]) < 20:  # if start point is <20 position, put it back to 0 as it's a clickling inaccuracy
            new_repert[i][1] = 0
        else:
            new_repert[i][1] = round(float(new_repert[i][1]))

        # SET END POINT
        ncin = Dataset('data/' + new_repert[i][0], 'r', format='NETCDF')
        # if high_limit> length depth vector, high limit automatically = len(depth vector)
        if round(float(new_repert[i][2])) > int(len(ncin.variables['depth'])):
            new_repert[i][2] = int(len(ncin.variables['depth']))
        else:
            new_repert[i][2]=round(float(new_repert[i][2]))

    pickle.dump(new_repert, open("/DATA/repertoires/"+name_pickle_file, "wb"))
    print('Pickle file /DATA/repertoires/' + name_pickle_file + 'created!')


def mark_shallow_deep_files(trimmed_repertoire_name):
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import pickle
    path = "/DATA/repertoires/"
    trimmed_repertoire_class=pd.read_pickle(path+trimmed_repertoire_name)
    repertoire_dict=extract_good_segment(trimmed_repertoire_name)

    repertoire_dict_class={}
    for i in range(len(repertoire_dict)):
        plt.plot(repertoire_dict[i][1:].astype(float)*(-1))
        plt.hlines(-10,0,4000,colors='r')
        plt.title(repertoire_dict[i][0])
        plt.grid()
        plt.show()

        classification=input('Deep (d) or Shallow (s) ?')
        repertoire_dict_class[i]=np.append(repertoire_dict[i],classification)
        trimmed_repertoire_class[i]=np.append(trimmed_repertoire_class[i],classification)
        plt.close()

    pickle.dump(trimmed_repertoire_class, open("DATA/repertoires/trimmed_repertoire_w_sdclass", "wb"))
    print('Pickle file /DATA/repertoires/trimmed_repertoire_w_sdclass created!')


def extract_good_segment(repertoire_str):
    #STEP 3: after improve start/end
    #MAKE DICTIONARY OF ALL GOOD FILES DEPTHS'
    import netCDF4 as nc
    import pandas as pd

    path ='./DATA/repertoires/'
    repertoire = pd.read_pickle(path + repertoire_str)
    repertoire_dict={}
    for i in range(len(repertoire)):
        ncin = nc.Dataset('./DATA/NARWdive_profiles_data/' + repertoire[i][0], 'r', format='NETCDF')
        low_limit = int(repertoire[i][1])
        high_limit = int(repertoire[i][2])
        a = np.array([repertoire[i][0], repertoire[i][3]])
        a1 = ncin['depth'][low_limit:high_limit]
        b = np.array(a1)
        repertoire_dict[i] = np.append(a, b)

    return repertoire_dict


    # path = "/home/loicka/Desktop/ws_whorld/repertoires/"
    # repertoire = pd.read_pickle(path + repertoire)
    # repertoire_dict={}
    # for i in range(len(repertoire)):
    #     ncin = Dataset('data/' + repertoire[i][0], 'r', format='NETCDF4')
    #     low_limit=int(repertoire[i][1])
    #     high_limit=int(repertoire[i][2])
    #     a=np.array([repertoire[i][0],repertoire[i][3]])
    #     b=np.array(ncin.variables['depth'][low_limit:high_limit])
    #     repertoire_dict[i]=np.append(a, b)
    #
    # return repertoire_dict

def occurences_count(vector):
    #find number of times one specific value occurs in a row
    vect0=[]
    vect1=[]
    vect2=[]
    vect3=[]

    values=np.array([0,1,2,3])
    for val in values:
        condition=np.array(vector==val)
        result=np.diff(np.where(np.concatenate(([condition[0]],condition[:-1] != condition[1:],[True])))[0])[::2]
        if val==0:
            vect0= result
        if val == 1:
            vect1 = result
        if val == 2:
            vect2 = result
        if val == 3:
            vect3 = result
    return vect0,vect1,vect2,vect3

def moving_average(vector, step):
    return np.convolve(vector, np.ones(step), 'valid') / step

def create_state_dps(repertoire):
    import copy
    surf_lim = 5
    sub_lim = 10

    depth={}
    depth_state={}
    for i in range(len(repertoire)):
        depth[i]=repertoire[i][2:].astype(float)
        depth_state[i]=copy.deepcopy(depth[i])
        depth_state[i][depth_state[i]<= surf_lim] = 1  # surface
        depth_state[i][(depth_state[i]> surf_lim) & (depth_state[i] <= sub_lim)] = 2  # subsurface
        depth_state[i][sub_lim < depth_state[i]] = 3  # deep
    return depth,depth_state


def count_transitions(depth_st):
    two_one=0
    two_three=0
    for l in range(len(depth_st) - 1):
        if depth_st[l,] == 2 and depth_st[l + 1,] == 1:  # here look for transitions 2>1
            two_one = two_one + 1
        elif depth_st[l,] == 2 and depth_st[l + 1,] == 3: #2>3
            two_three = two_three + 1

    return two_one,two_three

def create_vec0123s_plotting(depth_st):
    vec0={}
    vec1={}
    vec2={}
    vec3={}
    for i in range(len(depth_st)):
        vec0[i], vec1[i], vec2[i], vec3[i] = occurences_count(depth_st[i])
    return vec0,vec1,vec2,vec3

def create_vect0123s(depth_st):

    vect0 = []
    vect1 = []
    vect2 = []
    vect3 = []
    for i in range(len(depth_st)):
        vec0, vec1, vec2, vec3 = occurences_count(depth_st[i])
        vect0 = np.append(vect0, vec0)
        vect1 = np.append(vect1, vec1)
        vect2 = np.append(vect2, vec2)
        vect3 = np.append(vect3, vec3)

    #MOVING AVERAGE
    if len(vect0)!=0:
        vect0 = moving_average(vect0, 10)

    vect1 = np.round(moving_average(vect1, 10))
    vect2 = np.round(moving_average(vect2, 10))
    vect3 = np.round(moving_average(vect3, 10))

    return vect0,vect1,vect2,vect3

def plot_real_state_hist(depth_dict,depth_state_dict):
    fig = plt.figure(figsize=(20, 80), facecolor='w', edgecolor='k')
    fig.tight_layout()
    fig.subplots_adjust(hspace=.75)
    gs0 = fig.add_gridspec(len(depth_dict), 3) #number of files by # number of column (3 for real/state/histo)
    c = 0
    bins = np.arange(0, 500, 20)
    vec0,vec1,vec2,vec3=create_vec0123s_plotting(depth_state_dict)
    for i in range(len(depth_dict)):
        # REAL DIVE PROFILE
        ax1 = fig.add_subplot(gs0[c])
        ax1.plot((-1) * depth_dict[i])
        ax1.set_ylabel('Depth')
        ax1.set_xlabel('Time (s)')

        # STATE DIVE PROFILE
        ax2 = fig.add_subplot(gs0[c + 1])
        ax2.plot((-1) * depth_state_dict[i])
        ax2.set_ylabel('State')
        ax2.set_xlabel('Time (s)')

        # HISTOGRAMS VEC0/1/2/3
        gssub = gs0[c + 2].subgridspec(1, 4)
        for l in range(4):
            ax3 = fig.add_subplot(gssub[0, l])
            if l == 0:
                ax3.hist(vec0[i], bins)
                ax3.set_title('vect 0')
            elif l == 1:
                ax3.hist(vec1[i], bins)
                ax3.set_title('vect 1')
            elif l == 2:
                ax3.hist(vec2[i], bins)
                ax3.set_title('vect 2')
            elif l == 3:
                ax3.hist(vec3[i], bins)
                ax3.set_title('vect 3')
        c = c + 3

    plt.show()

def transform_dict_into_array(dict):
    array=[]
    for i in range(len(dict)):
        array=np.append(array,dict[i])
    return array
#
# #ALL
# repertoire_dict=extract_good_segment('trimmed_repertoire_w_sdclass') #yes
# depth_dict,depth_state_dict=create_state_dps(repertoire_dict) #yes
# depth_state_array=transform_dict_into_array(depth_state_dict)
# two_one,two_three=count_transitions(depth_state_array)
# #print('all',two_one,two_three)
# vect0,vect1,vect2,vect3=create_vect0123s(depth_state_dict)
# print('average',np.average(vect1),np.average(vect2),np.average(vect3))
#
# plot_real_state_hist(depth_dict,depth_state_dict)
#
# #SHALLOW:
# repertoire_dict=extract_good_segment('trimmed_repertoire_w_sdclass') #yes
# rep_shallow={}
# c=0
# for i in range(len(repertoire_dict)):
#     if repertoire_dict[i][1]=='s':
#         rep_shallow[c]=repertoire_dict[i]
#         c=c+1
# depth_dict,depth_state_dict=create_state_dps(rep_shallow) #yes
# depth_state_array=transform_dict_into_array(depth_state_dict)
# two_one,two_three=count_transitions(depth_state_array)
# #print('shallow',two_one,two_three)
# vect0,vect1,vect2,vect3=create_vect0123s(depth_state_dict) #yes
# print('shallow',np.average(vect1),np.average(vect2),np.average(vect3))
# # plot_real_state_hist(depth_dict,depth_state_dict)
#
# #DEEP
# repertoire_dict=extract_good_segment('trimmed_repertoire_w_sdclass') #yes
# rep_deep={}
# c=0
# for i in range(len(repertoire_dict)):
#     if repertoire_dict[i][1]=='d':
#         rep_deep[c]=repertoire_dict[i]
#         c=c+1
# depth_dict,depth_state_dict=create_state_dps(rep_deep) #yes
# depth_state_array=transform_dict_into_array(depth_state_dict)
# two_one,two_three=count_transitions(depth_state_array)
# #print('deep',two_one,two_three)
# vect0,vect1,vect2,vect3=create_vect0123s(depth_state_dict) #yes
# print('deep',np.average(vect1),np.average(vect2),np.average(vect3))
# # plot_real_state_hist(depth_dict,depth_state_dict)
#

#PLOTTTTTTTING
prefix='/home/loicka/Desktop/ws_whorld3/'
os.chdir(prefix)

from CODE.functions import f_dive_profile as dp
interval_blow=30
#SHALLOW:
repertoire_dict=extract_good_segment('trimmed_repertoire_w_sdclass') #yes
rep_shallow={}
c=0
for i in range(len(repertoire_dict)):
    if repertoire_dict[i][1]=='s':
        rep_shallow[c]=repertoire_dict[i]
        c=c+1
depth_dict,depth_state_dict=create_state_dps(rep_shallow) #yes
depth_array=depth_dict[16]
depth_state_array=depth_state_dict[16]

#CREATE ARTIFICIAL DP
vec_1,vec_2,vec_3,two_one,two_three=dp.info_for_dp_funct('shallow')
artificial_dp=dp.create_dive_profile(vec_1,vec_2,vec_3,two_one,two_three,interval_blow)

state_color='lightseagreen'

#PLOTTING
fig,ax=plt.subplots(3,2,sharex=True)
ax1,ax2,ax3,ax4,ax5,ax6=ax.flatten()

#((ax1,ax2),(ax3,ax4),(ax5,ax6))
#SHALLOW
ax1.plot(depth_array,color='mediumblue')
ax1.set_ylabel('Depth (m)')
ax1.annotate('A',(0,12),fontsize=13)
ax1.hlines(5,0,len(depth_array),colors='orange')
ax1.hlines(10,0,len(depth_array),colors='green')
ax1.invert_yaxis()

ax3.plot(depth_state_array,color=state_color)
ax3.set_ylabel('Modeled State')
ax3.annotate('C',(0,3),fontsize=13)
ax3.yaxis.set_ticks(np.arange(0, 4, 1))
ax3.invert_yaxis()

ax5.plot(artificial_dp[0:len(depth_array)],color=state_color)
ax5.set_ylabel('Remote State')
ax5.annotate('E',(0,3),fontsize=13)
ax5.yaxis.set_ticks(np.arange(0, 4, 1))
ax5.invert_yaxis()
ax5.set_xlabel('Time (s)')


#DEEP:
repertoire_dict=extract_good_segment('trimmed_repertoire_w_sdclass') #yes
rep_deep={}
c=0
for i in range(len(repertoire_dict)):
    if repertoire_dict[i][1]=='d':
        rep_deep[c]=repertoire_dict[i]
        c=c+1
depth_dict,depth_state_dict=create_state_dps(rep_deep) #yes
depth_array=depth_dict[7][0:len(depth_array)]
depth_state_array=depth_state_dict[7][0:len(depth_array)]

#CREATE ARTIFICIAL DP
vec_1,vec_2,vec_3,two_one,two_three=dp.info_for_dp_funct('deep')
artificial_dp=dp.create_dive_profile(vec_1,vec_2,vec_3,two_one,two_three,interval_blow)


#DEEP PLOT
ax2.plot(depth_array,color='mediumblue')
ax2.hlines(5,0,len(depth_array),colors='orange')
ax2.hlines(10,0,len(depth_array),colors='green')
ax2.annotate('B',(0,108),fontsize=13)
ax2.invert_yaxis()

ax4.plot(depth_state_array,color=state_color)
ax4.annotate('D',(0,3),fontsize=13)
ax4.yaxis.set_ticks(np.arange(0, 4, 1))
ax4.invert_yaxis()

ax6.plot(artificial_dp[0:len(depth_array)],color=state_color)
ax6.annotate('F',(0,3),fontsize=13)
ax6.yaxis.set_ticks(np.arange(0, 4, 1))
ax6.invert_yaxis()
ax6.set_xlabel('Time (s)')

# cols = ['Shallow Mode', 'Deep Mode']
# for axe, col in zip(ax[0], cols):
#     axe.set_title(col)

fig.subplots_adjust(bottom=0)
plt.tight_layout()
plt.show()
