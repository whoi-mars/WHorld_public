
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script plots all possible cases (45) obtained

Note: WORKS!
'''

#LIBRAIRIES
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def ship_speed_vs_prob_plot(path,folder1):
    def st_to_array(string):
        li = list(string.split(","))
        li = [int(x) for x in li]
        array = np.asarray(li)
        return array

    def row_column(rt,sh,reaction_time_array,ship_height_array,mode):
        if mode=='mixed':
            if rt == reaction_time_array[0]:
                column = 0
            elif rt==reaction_time_array[1]:
                column=3
            else:
                column = 6
        elif mode=='deep':
            if rt == reaction_time_array[0]:
                column = 2
            elif rt == reaction_time_array[1]:
                column=5
            else:
                column = 8
        elif mode=='shallow':
            if rt == reaction_time_array[0]:
                column = 1
            elif rt == reaction_time_array[1]:
                column=4
            else:
                column = 7

        if sh==ship_height_array[0]:
            row=0
        elif sh==ship_height_array[1]:
            row=1
        elif sh==ship_height_array[2]:
            row=2
        elif sh==ship_height_array[3]:
            row=3
        elif sh==ship_height_array[4]:
            row=4
        else:
            print('ERROR IN SHIP HEIGHTS OR REACTION TIME: CORRECT row_column function')
        return row, column

    def add_2axis(value,ax1):
    #FUNCTION THAT ADD SECOND X AXIS
        if value == 1: #place second labeled axis
            ax2 = ax1.twiny()

            newlabel = np.round(np.linspace(1.94, 29.15, 6)).astype(int)
            k2degc = lambda t: t * 0.5144
            newpos = [k2degc(t) for t in newlabel]
            ax2.set_xticks(newpos)
            ax2.set_xticklabels(newlabel)

            ax2.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
            ax2.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
            ax2.spines['bottom'].set_position(('outward', 60))
            ax2.set_xlabel('Ship speed (kn)',**font)
            #ax2.xaxis.get_label().set_fontsize(16)
            ax2.xaxis.set_label_coords(0.49,-0.65)

    def read_csv_header(csv_dir):
        import csv
        with open(csv_dir, 'r') as f:
            d_reader = csv.DictReader(f)
            headers = d_reader.fieldnames
        return headers

    def extract_ship_reaction_time(header_list):
        rts = [i for i in header_list if i.startswith('ship reaction')]
        ship_rt = []
        for i in rts:
            ship_rt1 = int(pd.Series(df[i]).array[-1])
            ship_rt = np.append(ship_rt, ship_rt1)
        return ship_rt

    #Case Excel sheet
    csv_dir=str(path+folder1+'/cases_file_'+folder1+'.csv')
    header_list=read_csv_header(csv_dir)
    df = pd.read_csv(csv_dir,names=header_list,header=0)

    #Important parameters:
    inter_blow=np.asarray(pd.Series(df['Interval btw blows (s)']).array[-4:])
    reaction_time= extract_ship_reaction_time(header_list).astype(int)
    ship_heights=st_to_array(pd.Series(df['ship height (m)']).array[-1])
    speeds=[st_to_array(pd.Series(df['ship speeds (m/s)']).array[-1])]

    #START
    names=[]
    #FOLDER 1
    #Variables needed for running code:
    av_probs_fd1 = {}
    std_probs_fd1 = {}

    directory1 = path + folder1 + '/'
    for filename in os.listdir(directory1):
        if filename.endswith(".pickle"):# and filename.startswith('IBI'):
            object = pd.read_pickle(directory1 + filename)
            name = object['run name']
            names.append(name)
            av_probs_fd1[name] = object['Probs average of detection']
            std_probs_fd1[name] = object['Probs std of detection']
    detection = ['RDR', 'DDF']

    #  PLOTTING
    font = {'family': 'sans-serif',
            'weight': 'normal',
            'size': 20}
    plt.rc('font', **font)
    fig1, ax1 = plt.subplots(len(ship_heights), len(reaction_time) * 3, figsize=(33, 18))
    color = ['indigo', 'darkviolet', 'mediumorchid', 'plum', 'darkgreen', 'forestgreen', 'limegreen', 'springgreen']

    modes= np.array(['mixed', 'deep', 'shallow'])
    for mode in modes:
        for s in ship_heights:
            for rt in reaction_time:
                i_color = 0
                subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(s)
                for d in detection:
                    for i in inter_blow:
                        dict1 = 'IBI_' + str(i) + '_' + d + '_' + mode
                        info=av_probs_fd1[dict1][subdict]

                        row, column = row_column(rt, s, reaction_time, ship_heights, mode)
                        line1, = ax1[row, column].plot(np.asarray(speeds).T, info, color=color[i_color],
                                                       label='IBI:' + str(i) + ',' + d)
                        i_color = i_color + 1

                        # Grid
                        ax1[row, column].grid()

                        # axis ticks
                        if row != 4:
                            ax1[row, column].set_xticklabels([])
                        if column != 0:
                            ax1[row, column].set_yticklabels([])

                        # # title
                        # ax1[row, column].set_title('RT:' + str(int(rt / 60)) + 'min, MD=' + str(s) + 'm,' + mode,
                        #                            **font)

                        # y axis:
                        ax1[row, 0].set(ylabel='In-time detection' + '\n' + 'probability')
                        # ax1[row, 0].yaxis.get_label().set_fontsize(16)

                        # x axis:
                        ax1[4, column].set(xlabel='Ship speed (m/s)')
                        # ax1[4, column].xaxis.get_label().set_fontsize(16)

    # Set y axis limits
    for axx in ax1.flat:
        axx.grid()
        axx.set_ylim(-0.05, 1.05)

    # SUBPLOT FORMATTING
    cols = [reaction_time[0]/60,reaction_time[0]/60,reaction_time[0]/60,reaction_time[1]/60,reaction_time[1]/60,reaction_time[1]/60,reaction_time[2]/60,reaction_time[2]/60,reaction_time[2]/60]
    mode_type=['mixed','shallow','deep','mixed','shallow','deep','mixed','shallow','deep']
    cols = list(map(int, cols))
    rows = ship_heights.tolist()  # [f for f in ship_heights]

    pad = 5  # in points
    i=0
    for ax, col in zip(ax1[0], cols):
        ax.annotate(mode_type[i]+'\n'+'RT:'+str(col)+'min', xy=(0.5, 1), xytext=(0, pad),
                        xycoords='axes fraction', textcoords='offset points',
                        size='large', ha='center', va='baseline')
        i=i+1

    for ax, row in zip(ax1[:, 0], rows):
        ax.annotate('MRR:'+'\n'+str(row)+'m', xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                        xycoords=ax.yaxis.label, textcoords='offset points',
                        size='large', ha='right', va='center')


    # Turn off tick labels
    ax1[0, 0].set_xticklabels([])
    ax1[0, 0].annotate('A', (1, 0), fontsize=30)

    # Legend
    plt.subplots_adjust(right=0.88)
    ax1[4, 1].legend(title='Legend:', bbox_to_anchor=(9.5, 3.0), loc="center left", borderaxespad=0.)  # ncol=2

    # Add Second axis
    for i in range(3*len(reaction_time)):
        add_2axis(1, ax1[4, i])

    # Number of epochs ran
    epochs = (pd.Series(df['epoch number']).array[-1])
    fig1.suptitle('Superplot' + '\n' + str(epochs) + 'epochs' + '\n' + 'from run: ' + folder1)
    plt.tight_layout()

    # plt.savefig(path+folder1+'/MODE:'+mode+'.png')#,bbox_inches='tight')
    plt.show()



#RUN CODE HERE
#Inputs
prefix='/home/loicka/Desktop/ws_whorld3'
path=prefix+'/OUTPUTS/RUN_RESULTS/'
folder1='June_7th_50ep'

ship_speed_vs_prob_plot(path,folder1)