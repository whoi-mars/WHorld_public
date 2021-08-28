
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
not sure yet

Note: Does NOT work
'''




# def customized_plot(parameter,folder_path):
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
prefix='/home/loicka/Desktop/ws_whorld/organized_whorld'

folder = 'June_7th_50ep'
parameter = 'IBI'
#todo change name here and IBI if needed
name1 = 'ep300,rt3600,w100,s3,allblow:F,allsurf:F,allsub:F,alldeep:F,wmean_v:1,wstd_v:0.2,'
inter_blow = [17, 30, 60, 120]

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 15}
plt.rc('font', **font)

av_probs = {}
std_probs = {}

RDR_60_1500 = {}
RDR_120_1500 = {}
RDR_60_3000 = {}
RDR_120_3000 = {}

DDF_60_1500 = {}
DDF_120_1500 = {}
DDF_60_3000 = {}
DDF_120_3000 = {}


def add_2axis(value,ax1):
#FUNCTION THAT ADD SECOND X AXIS
    if value == 1: #place second labeled axis
        ax2 = ax1.twiny()

        newlabel = np.round(np.linspace(1.94, 29.15, 6))
        k2degc = lambda t: t * 0.5144
        newpos = [k2degc(t) for t in newlabel]
        ax2.set_xticks(newpos)
        ax2.set_xticklabels(newlabel)

        ax2.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
        ax2.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
        ax2.spines['bottom'].set_position(('outward', 45))
        ax2.set_xlabel('Ship speed (kn)',**font)
        ax2.xaxis.get_label().set_fontsize(15)
        ax2.xaxis.set_label_coords(0.49,-0.22)
       # ax2.set_fontname('Arial')
        #ax2.xaxis.get_label().set_position('left')
    # if value==2: #place second non-labelled axis
    #     ax2 = ax1.twiny()
    #     newlabel = np.round(np.linspace(1.94, 29.15, 5))
    #     k2degc = lambda t: t * 0.5144
    #     newpos = [k2degc(t) for t in newlabel]
    #     ax2.set_xticks(newpos)
    #     ax2.set_xticklabels(newlabel)
    #
    #     ax2.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
    #     ax2.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
    #     ax2.spines['bottom'].set_position(('outward', 36))
    #     ax2.set_xticklabels([])

# LOAD AV & STD PROBS FOR ALL FILES IN A FOLDER
directory = prefix+'/OUTPUTS/RUN_RESULTS/' + folder + '/'
for filename in os.listdir(directory):
    if filename.endswith(".pickle"):
        object = pd.read_pickle(directory + filename)
        name = object['run name']
        av_probs[name] = object['Probs average of detection']
        std_probs[name] = object['Probs std of detection']
        #speeds = object['ship speeds (m/s)']

if parameter == 'IBI':

    RDR=[]
    DDF=[]
    for i in range(len(inter_blow)):
        RDR.append('inter_blow:' + str(inter_blow[i])+ ',DDF:0')
        DDF.append('inter_blow:' + str(inter_blow[i])+ ',DDF:1')

    types = ['reaction_time:60ship_height:1500','reaction_time:60ship_height:3000','reaction_time:120ship_height:1500','reaction_time:120ship_height:3000']
    color = ['indigo', 'darkviolet', 'mediumorchid', 'plum', 'darkgreen', 'forestgreen', 'limegreen','springgreen']
    fig1, ax1 = plt.subplots(2, 2,figsize=(12,12))
    RDR_lines = []
    DDF_lines = []

    for i in range(len(RDR)):
        RDR_60_1500[RDR[i]] = av_probs[str(name1) + RDR[i]][types[0]]
        RDR_120_1500[RDR[i]] = av_probs[str(name1) + RDR[i]][types[2]]
        RDR_60_3000[RDR[i]] = av_probs[str(name1) + RDR[i]][types[1]]
        RDR_120_3000[RDR[i]] = av_probs[str(name1) + RDR[i]][types[3]]

        DDF_60_1500[DDF[i]] = av_probs[str(name1) + DDF[i]][types[0]]
        DDF_120_1500[DDF[i]] = av_probs[str(name1) + DDF[i]][types[2]]
        DDF_60_3000[DDF[i]] = av_probs[str(name1) + DDF[i]][types[1]]
        DDF_120_3000[DDF[i]] = av_probs[str(name1) + DDF[i]][types[3]]

        # 60/1500
        line1, = ax1[0, 0].plot(speeds, RDR_60_1500[RDR[i]], color=color[i], label='IBI:' + RDR[i][11:14])
        line2, = ax1[0, 0].plot(speeds, DDF_60_1500[DDF[i]], color=color[i + 4])
        if i==3:
            RDR_lines.append(line1)
            DDF_lines.append(line2)

        ax1[0, 0].set_title('RT: 1min, MD=1500m')
        ax1[0,0].set(ylabel='In-time probability')
        ax1[0, 0].yaxis.get_label().set_fontsize(16)
        # Turn off tick labels
        ax1[0,0].set_xticklabels([])
        ax1[0,0].annotate('A',(1,0),fontsize=30)

        # 60/3000
        line1, = ax1[0, 1].plot(speeds, RDR_60_3000[RDR[i]], color=color[i], label='IBI:' + RDR[i][11:14])
        line2, = ax1[0, 1].plot(speeds, DDF_60_3000[DDF[i]], color=color[i + 4])
        if i == 3:
            RDR_lines.append(line1)
            DDF_lines.append(line2)
        ax1[0, 1].set_title('RT: 1min, MD=3000m')
        # Turn off tick labels
        ax1[0,1].set_yticklabels([])
        ax1[0,1].set_xticklabels([])
        ax1[0,1].annotate('B',(1,0),fontsize=30)

        # 120/1500
        line1, = ax1[1, 0].plot(speeds, RDR_120_1500[RDR[i]], color=color[i], label='IBI:' + RDR[i][11:14])
        line2, = ax1[1, 0].plot(speeds, DDF_120_1500[DDF[i]], color=color[i + 4])
        RDR_lines.append(line1)
        DDF_lines.append(line2)
        ax1[1, 0].set_title('RT: 2min, MD=1500m')
        ax1[1,0].set(xlabel='Ship speed (m/s)', ylabel='In-time probability')
        ax1[1, 0].xaxis.get_label().set_fontsize(15)
        ax1[1, 0].yaxis.get_label().set_fontsize(16)
        ax1[1,0].xaxis.set_label_coords(0.5, -0.07)
        add_2axis(1,ax1[1,0])
        ax1[1,0].annotate('C',(1,0),fontsize=30)

        # 120/3000
        line1, = ax1[1, 1].plot(speeds, RDR_120_3000[RDR[i]], color=color[i], label='IBI:' + RDR[i][11:14])
        line2, = ax1[1, 1].plot(speeds, DDF_120_3000[DDF[i]], color=color[i + 4])
        if i == 3:
            RDR_lines.append(line1)
            DDF_lines.append(line2)

        ax1[1, 1].set_title('RT: 2min, MD=3000m')
        ax1[1,1].set(xlabel='Ship speed (m/s)')
        ax1[1,1].xaxis.get_label().set_fontsize(15)
        add_2axis(1,ax1[1,1])
        ax1[1, 1].set_yticklabels([])
        ax1[1,1].annotate('D',(1,0),fontsize=30)

for ax in ax1.flat:
    ax.grid()
    ax.set_ylim(-0.05,1.05)
    #SET SECOND AXIS
# legend1 = plt.legend(RDR_lines[:], inter_blow, title="RDR, IBI (s):", bbox_to_anchor=(1, 0.5),frameon=False)
# legend2 = plt.legend(DDF_lines[:], inter_blow, title="DDF, IBI (s):", bbox_to_anchor=(1, 2),frameon=False)
# #plt.legend(DDF_lines[:], inter_blow, title="DDF, IBI (s):",loc='upper left')#, bbox_to_anchor=(1, 1))
# plt.gca().add_artist(legend1)
# plt.gca().add_artist(legend2)
a=np.append(RDR_lines[0:4],DDF_lines[0:4])
b=np.append(inter_blow,inter_blow)
ax1[0,1].legend(a, b,ncol=2, title='RDR DDF IBI (s):', frameon=True,loc='lower right')

plt.tight_layout()
plt.show()

print('bgf')