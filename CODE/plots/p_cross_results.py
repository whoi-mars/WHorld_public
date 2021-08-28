'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script plots cross-result plots

Note: DOES WORK
'''



import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openpyxl
from adjustText import adjust_text

prefix='/home/loicka/Desktop/ws_whorld/organized_whorld'
os.chdir(prefix)
excelbook=openpyxl.load_workbook(prefix+'/OUTPUTS/values_storage.xlsx')
excelsheet= excelbook.worksheets[0]


def read_csv_header(csv_dir):
    import csv
    with open(csv_dir, 'r') as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
    return headers

def extract_ship_reaction_time(header_list,df):
    rts = [i for i in header_list if i.startswith('ship reaction')]
    ship_rt = []
    for i in rts:
        ship_rt1 = int(pd.Series(df[i]).array[-1])
        ship_rt = np.append(ship_rt, ship_rt1)
    return ship_rt

def str_to_array(string):
    li = list(string.split(","))
    li = [int(x) for x in li]
    array = np.asarray(li)
    return array

def extract_data(path,folder1):
    #  PLOTTING FORMAT
    font = {'family': 'sans-serif',
            'weight': 'normal',
            'size': 15}
    plt.rc('font', **font)

    #Case Excel sheet
    csv_dir=str(path+'/'+folder1+'/'+'cases_file_'+folder1+'.csv')
    header_list=read_csv_header(csv_dir)
    df = pd.read_csv(csv_dir,names=header_list,header=0)

    #Important parameters:
    reaction_time= extract_ship_reaction_time(header_list,df).astype(int)
    speeds=pd.Series(df['ship speeds (m/s)']).array[-1]
    ship_heights=pd.Series(df['ship height (m)']).array[-1]
    IBIs=np.unique(pd.Series(df['Interval btw blows (s)']))
    if isinstance(speeds,str)==1:
        speeds=str_to_array(speeds)

    if isinstance(ship_heights, str) == 1:
        ship_heights = str_to_array(ship_heights)

    #Variables needed for running code:
    av_probs_fd1 = {}
    std_probs_fd1 = {}
    names = []

    directory1 = path + folder1 + '/'
    for filename in os.listdir(directory1):
        if filename.endswith(".pickle"):# and filename.startswith('IBI'):
            object = pd.read_pickle(directory1 + filename)
            name = object['run name']
            names.append(name)
            av_probs_fd1[name] = object['Probs average of detection']
            std_probs_fd1[name] = object['Probs std of detection']
    return reaction_time,speeds,ship_heights,IBIs,av_probs_fd1,std_probs_fd1,font

def display_pt_value(x,y,axis):
    label = "{:.2f}".format(y)

    axis.annotate(label, # this is the text
                     (x,y), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(2,-20), # distance from text to points (x,y)
                     ha='center', # horizontal alignment can be left, right or center
                     fontsize=15)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fig1, ((ax1,ax2),(ax3,ax4),(ax5,ax6))= plt.subplots(nrows=3, ncols=2,figsize=(10,15))
plt.subplots_adjust(hspace=0.25,bottom=0.06)
linestyles=['solid','dashed','dashdot','dotted']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %% CASE 1:  DDF vs.RDR for all RT at Ship Height=1km, ship speed=10kn
#FIXED: detection range=1000m, IBI: 60s, mixed, DDF/RDR

# Inputs
path = prefix+'/OUTPUTS/RUN_RESULTS/'

folder1 = 'RDR_DDF_RT'
reaction_time,speeds,ship_heights,IBIs,av_probs_fd1,std_probs_fd1,font=extract_data(path, folder1)

reaction_time_special = np.arange(0, 600, 10)
detection_modes=['DDF','RDR']
dive_mode = 'mixed'
sh = 1000
inter_blow=60
info_1=[]
info_2=[]

interest_pt=[5,29,59] #correspond to 60,300,600 RT
for rt in reaction_time_special:
        dict_DDF = 'IBI_' + str(inter_blow) + '_' + detection_modes[0] + '_' + dive_mode
        dict_RDR = 'IBI_' + str(inter_blow) + '_' + detection_modes[1] + '_' + dive_mode
        subdict_1 = 'reaction_time:' + str(rt) + 'ship_height:' + str(sh)
        info_1=np.append(info_1,av_probs_fd1[dict_DDF][subdict_1])
        info_2=np.append(info_2,av_probs_fd1[dict_RDR][subdict_1])

cell_id=['B2','B3','C2','C3','D2','D3']
#display point of comparison
n=0
texts1=[]
texts2=[]
for i in interest_pt:
    display_pt_value(reaction_time_special[i],info_1[i],ax1)
    display_pt_value(reaction_time_special[i],info_2[i],ax1)
    ax1.plot(reaction_time_special[i],info_1[i],marker='o',color='r')
    ax1.plot(reaction_time_special[i], info_2[i], marker='o', color='r')
    text1 = [ax1.text(reaction_time_special[i], info_1[i], round(info_1[i], 2))]
    texts1.append(text1)
    #adjust_text(text1)

    text2 = [ax1.text(reaction_time_special[i], info_2[i], info_2[i])]
    texts2.append(text2)
    #adjust_text(text2)

    #save pt of comparison
    excelsheet[cell_id[n]].value = info_1[i]
    excelsheet[cell_id[n+1]].value=info_2[i]
    n=n+2

# adjust_text(texts1, ax=ax1)
# adjust_text(texts2, ax=ax1)

ax1.plot(reaction_time_special, info_1, label=str(detection_modes[0]),ls=linestyles[0])

ax1.plot(reaction_time_special, info_2, label=str(detection_modes[1]),ls=linestyles[1])



labels = np.arange(0,720,120)/60
ax1.set_xticks(np.arange(0,720,120))
ax1.set_xticklabels(labels)
ax1.set_xlabel('Reaction time (min)', **font)
ax1.set_ylabel('ITDP', **font)
ax1.grid()
ax1.set_xlim([0,600])

ax1.annotate('A', xy=(-0.08,0.86), xycoords='axes fraction',weight='bold', fontsize=20)
#ax1.annotate('A',(-0.08, 0.86), xycoords=an1.get_window_extent,fontsize=20, weight='bold')
ax1.legend(loc='center left',fontsize=15)
ax1.set_ylim(0, 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#%% CASE 2: Whale speeds
#Fixed= DDF, mixed, RDR=1000m, RT=300s, IBI=60s
#Inputs
folder1 = 'June_7th_50ep'
reaction_times,speeds,ship_heights,IBIs,av_probs_fd1,std_probs_fd1,font=extract_data(path, folder1)
color = ['darkgreen', 'blue','purple','orange']
dive_mode = 'mixed'
detection_mode='DDF'
ship_height=1000
rt=300
whale_speeds=np.array([0,1,2,3])
subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(ship_height)
i_color=0
for wp in whale_speeds:
    dict1 = 'WhaleSpeed_' + str(wp)
    info = av_probs_fd1[dict1][subdict]
    ax2.plot(np.asarray(speeds).T, info, color=color[i_color],
             label=str(wp) + 'm/s',ls=linestyles[i_color])
    i_color = i_color + 1

ax2.set_xticks(np.arange(0,16,3))
ax2.set_xlabel('Ship speed (m/s)', **font)
ax2.grid()
ax2.annotate('B', xy=(-0.08,0.86), xycoords='axes fraction',weight='bold', fontsize=20)
ax2.legend(title='Whale Speed:',title_fontsize=15,loc='center left',fontsize=15)
ax2.set_ylim(0, 1)
ax2.set_xlim(0, 15)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#%% CASE 3: IBI & RT: x=IBI, y=ITDP
#Fixed= mixed, DDF, RDR=1000m, RT= 1,5,10min, IBI= 30,60,120,300s
#Inputs
path = prefix+'/OUTPUTS/RUN_RESULTS/'
folder1 = 'June_7th_50ep'
reaction_times,speeds,ship_heights,IBIs,av_probs_fd1,std_probs_fd1,font=extract_data(path, folder1)
color = ['darkgreen', 'blue','purple']
position=9 #10m/s, 20kn
dive_mode = 'mixed'
detection_mode='DDF'
ship_height=1000

i_color=0
cell_id=['Y2','Z2','AA2','AB2','Y3','Z3','AA3','AB3','Y4','Z4','AA4','AB4']
n=0
for rt in reaction_times:
    info_DDF=[]
    for IBI in IBIs:
        subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(ship_height)
        dict_DDF = 'IBI_' + str(IBI) + '_' + detection_mode + '_' + dive_mode
        info=av_probs_fd1[dict_DDF][subdict][position]  # only keep prob for 10m/s, located in position 4
        info_DDF=np.append(info_DDF,info)
        # display point of comparison
        display_pt_value(IBI, info,ax3)
        ax3.plot(IBI, info, marker='o', color='r')
        # save pt of comparison
        excelsheet[cell_id[n]].value = info
        n = n + 1

    ax3.plot(IBIs, info_DDF, label='RT:'+str(int(rt/60))+'min', color=color[i_color],ls=linestyles[i_color])
    i_color=i_color+1

labels = np.arange(0,400,60)/60
ax3.set_xticks(np.arange(0,400,60))
ax3.set_xticklabels(labels)

ax3.set_xlabel('Inter-blow interval (min)', **font)
ax3.set_ylabel('ITDP', **font)
ax3.grid()
ax3.annotate('C', xy=(-0.08,0.86), xycoords='axes fraction',weight='bold', fontsize=20)
ax3.legend(loc='center left',fontsize=15)
ax3.set_ylim(0, 1)
ax3.set_xlim(0, 300)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#%% CASE 4: WHALE DIVING BEHAVIOR, x=ship speeds, y= ITDP
#FIXED: RT=300s, IBI=60s, DDF, RDR=1000m
#Inputs
folder1 = 'June_7th_50ep'
reaction_time,speeds,ship_heights,IBIs,av_probs_fd1,std_probs_fd1,font=extract_data(path, folder1)
color = ['darkgreen', 'blue','purple']
inter_blow = 60
detection_mode = 'DDF'
ship_height = 1000
rt = 300

modes = np.array(['mixed', 'deep', 'shallow'])

i= 0
cell_id=['M2','N2','O2']
cell_id2=['M6','N6','O6']
cell_id3=['M10','N10','O10']
for mode in modes:
    subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(ship_height)
    dict1 = 'IBI_' + str(inter_blow) + '_' + detection_mode + '_' + mode
    info = av_probs_fd1[dict1][subdict]
    ax4.plot(np.asarray(speeds).T, info, label=str(mode), color=color[i],ls=linestyles[i])
    #@10kn
    # display point of comparison
    display_pt_value(speeds[4], info[4],ax4)
    ax4.plot(speeds[4], info[4], marker='o', color='r')
    # save pt of comparison
    excelsheet[cell_id[i]].value = info[4]
    #@20knot
    # #display point of comparison
    display_pt_value(speeds[9],info[9],ax4)
    ax4.plot(speeds[9],info[9],marker='*',color='r')
    #save pt of comparison
    excelsheet[cell_id2[i]].value=info[9]

    # @15m/s
    # #display point of comparison
    display_pt_value(speeds[14], info[14],ax4)
    ax4.plot(speeds[14], info[14], marker='v', color='r')
    # save pt of comparison
    excelsheet[cell_id3[i]].value = info[14]
    i = i + 1

ax4.set_xlabel('Ship speed (m/s)', **font)
ax4.legend(loc='center left',fontsize=15)
ax4.grid()
ax4.annotate('D', xy=(-0.08,0.86), xycoords='axes fraction',weight='bold', fontsize=20)
ax4.set_ylim(0, 1)
ax4.set_xlim(0, 15)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#%% CASE 5: RDR vs ITDP for different RTs
#Fixed: detection range=1000, 5/10 m/s, mixed, IBI=60
#Inputs
folder1 = 'June_7th_50ep'
reaction_time,speeds,ship_heights,IBIs,av_probs_fd1,std_probs_fd1,font=extract_data(path, folder1)
color = ['mediumorchid', 'blue','purple','cyan']
inter_blow = 60
dive_mode = 'mixed'
i= 0
reaction_time=[60,600]
detection_mode='DDF'
cell_id5=['R2','S2','T2','U2','V2','R4','S4','T4','U4','V4']
cell_id10=['R3','S3','T3','U3','V3','R5','S5','T5','U5','V5']
n=0

info5=[]
info10=[]
info_rt1s=[]


for rt in reaction_time:
     for sh in ship_heights:
        if rt==60:
            subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(sh)
            dict_DDF = 'IBI_' + str(inter_blow) + '_' + detection_mode + '_' + dive_mode
            info_rt1 = av_probs_fd1[dict_DDF][subdict][4]
            info_rt1s.append(info_rt1)
            display_pt_value(sh, info_rt1, ax5)
            ax5.plot(sh, info_rt1, marker='o', color='r')
        else:
            subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(sh)
            dict_DDF = 'IBI_' + str(inter_blow) + '_' + detection_mode + '_' + dive_mode
            info_5ms = av_probs_fd1[dict_DDF][subdict][4]  # only keep prob for 5m/s, located in position 4
            info_10ms = av_probs_fd1[dict_DDF][subdict][9]
            info5.append(info_5ms)
            info10.append(info_10ms)
            # display point of comparison
            display_pt_value(sh, info_5ms, ax5)
            ax5.plot(sh, info_5ms, marker='o', color='r')
            display_pt_value(sh, info_10ms, ax5)
            ax5.plot(sh, info_10ms, marker='o', color='r')
            # save pt of comparison
            excelsheet[cell_id5[n]].value = info_5ms
            excelsheet[cell_id10[n]].value = info_10ms
            n = n + 1
ax5.plot(ship_heights, info_rt1s, label='RT:' + str(int(60 / 60)) + 'min,@' + str(speeds[4]) + ' & '+str(speeds[9])+'m/s', color=color[0],
             ls=linestyles[0])
ax5.plot(ship_heights, info5, label='RT:'+ str(int(600/60))+'min,@'+str(speeds[4])+'m/s', color=color[1],ls=linestyles[1])
ax5.plot(ship_heights, info10, label='RT:' + str(int(600/60)) + 'min,@'+str(speeds[9])+'m/s', color=color[2],ls=linestyles[2])

# for rt in reaction_time:
#     for sh in ship_heights:
#         if rt==60:
#             subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(sh)
#             dict_DDF = 'IBI_' + str(inter_blow) + '_' + detection_mode + '_' + dive_mode
#             info_rt1 = av_probs_fd1[dict_DDF][subdict][4]
#             info_rt1s.append(info_rt1)
#             display_pt_value(sh, info_rt1, ax5)
#             ax5.plot(sh, info_rt1, marker='o', color='r')
#         else:
#             subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(sh)
#             dict_DDF = 'IBI_' + str(inter_blow) + '_' + detection_mode + '_' + dive_mode
#             info_5ms = av_probs_fd1[dict_DDF][subdict][4]  # only keep prob for 5m/s, located in position 4
#             info_10ms = av_probs_fd1[dict_DDF][subdict][9]
#             info5.append(info_5ms)
#             info10.append(info_10ms)
#             # display point of comparison
#             display_pt_value(sh, info_5ms,ax5)
#             ax5.plot(sh, info_5ms, marker='o', color='r')
#             display_pt_value(sh, info_10ms,ax5)
#             ax5.plot(sh, info_10ms, marker='o', color='r')
#             # save pt of comparison
#             excelsheet[cell_id5[n]].value = info_5ms
#             excelsheet[cell_id10[n]].value = info_10ms
#             n=n+1
#
# ax5.plot(ship_heights, info_rt1s, label='RT:' + str(int(60 / 60)) + 'min,@' + str(speeds[4]) + ' & '+str(speeds[9])+'m/s', color=color[0],
#              ls=linestyles[0])
# ax5.plot(ship_heights, info5, label='RT:'+ str(int(rt/60))+'min,@'+str(speeds[4])+'m/s', color=color[1],ls=linestyles[1])
# ax5.plot(ship_heights, info10, label='RT:' + str(int(rt/60)) + 'min,@'+str(speeds[9])+'m/s', color=color[2],ls=linestyles[2])

ax5.set_xticks(np.arange(0,3500,500))
ax5.set_xlabel('RDR (m)', **font)
ax5.grid()
ax5.set_ylabel('ITDP', **font)
ax5.annotate('E', xy=(-0.08,0.86), xycoords='axes fraction',weight='bold', fontsize=20)
ax5.legend(loc='center left',fontsize=15)
ax5.set_ylim(0, 1)
ax5.set_xlim(0, 3000)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#%% CASE 6: REACTION TIME, y=ITDP, x= ship speed
#FIXED: IBI=60s,DDF,RDR=1000m, mixed, RT= 1,5,10min

#Inputs
folder1 = 'June_7th_50ep'
reaction_time,speeds,ship_heights,IBIs,av_probs_fd1,std_probs_fd1,font=extract_data(path, folder1)
color = ['darkgreen', 'blue','purple']
dive_mode = 'mixed'
inter_blow = 60
detection_mode = 'DDF'
ship_height = 1000

i = 0
cell_id=['H2','I2','J2']
cell_id2=['H5','I5','J5']
cell_id3=['H8','I8','J8']
for rt in reaction_time:
    subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(ship_height)
    dict1 = 'IBI_' + str(inter_blow) + '_' + detection_mode + '_' + dive_mode
    info = av_probs_fd1[dict1][subdict]
    ax6.plot(np.asarray(speeds).T, info, label='RT:'+ str(int(rt / 60)) + 'min', color=color[i],ls=linestyles[i])
    #@5m/2
    # #display point of comparison
    display_pt_value(speeds[4],info[4],ax6)
    ax6.plot(speeds[4],info[4],marker='o',color='r')
    #save pt of comparison
    excelsheet[cell_id[i]].value=info[4]

    #@10m/s
    # #display point of comparison
    display_pt_value(speeds[9],info[9],ax6)
    ax6.plot(speeds[9],info[9],marker='*',color='r')
    #save pt of comparison
    excelsheet[cell_id2[i]].value=info[9]

    # @15m/s
    # #display point of comparison
    display_pt_value(speeds[14], info[14],ax6)
    ax6.plot(speeds[14], info[14], marker='v', color='r')
    # save pt of comparison
    excelsheet[cell_id3[i]].value = info[14]

    i = i + 1
ax6.set_xlabel('Ship speed (m/s)', **font)
ax6.legend(loc='center left',fontsize=15)
ax6.grid()
ax6.annotate('F', xy=(-0.08,0.86), xycoords='axes fraction',weight='bold', fontsize=20)
ax6.set_ylim(0, 1)
ax6.set_xlim(0, 15)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
plt.show()
#save excel changes
excelbook.save('values_storage.xlsx')