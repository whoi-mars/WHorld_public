
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script plots ITDP results as a function of whale speeds

Note: WORKS!
'''



#LIBRAIRIES
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl

def read_csv_header(csv_dir):
    import csv
    with open(csv_dir, 'r') as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
    return headers


def extract_ship_reaction_time(header_list, df):
    rts = [i for i in header_list if i.startswith('ship reaction')]
    ship_rt = []
    for i in rts:
        ship_rt1 = int(pd.Series(df[i]).array[-1])
        ship_rt = np.append(ship_rt, ship_rt1)
    return ship_rt


def st_to_array(string):
    li = list(string.split(","))
    li = [int(x) for x in li]
    array = np.asarray(li)
    return array


def row_column(rt, sh, reaction_time_array, ship_height_array):
    if rt == reaction_time_array[0]:
        column = 0
    else:
        column = 1

    if sh == ship_height_array[0]:
        row = 0
    elif sh == ship_height_array[1]:
        row = 1
    elif sh == ship_height_array[2]:
        row = 2
    elif sh == ship_height_array[3]:
        row = 3
    elif sh == ship_height_array[4]:
        row = 4
    else:
        print('ERROR IN SHIP HEIGHTS OR REACTION TIME: CORRECT row_column function')
    return row, column


def add_2axis(value, ax1,font):
    # FUNCTION THAT ADD SECOND X AXIS
    if value == 1:  # place second labeled axis
        ax2 = ax1.twiny()

        newlabel = np.round(np.linspace(1.94, 29.15, 6))
        k2degc = lambda t: t * 0.5144
        newpos = [k2degc(t) for t in newlabel]
        ax2.set_xticks(newpos)
        ax2.set_xticklabels(newlabel,**font)

        ax2.xaxis.set_ticks_position('bottom')  # set the position of the second x-axis to bottom
        ax2.xaxis.set_label_position('bottom')  # set the position of the second x-axis to bottom
        ax2.spines['bottom'].set_position(('outward', 60))
        ax2.set_xlabel('Ship speed (kn)', **font)
        # ax2.xaxis.get_label().set_fontsize(16)
        ax2.xaxis.set_label_coords(0.49, -0.56)


def ship_speed_vs_prob_plot(folder,path,mode,inter_blow, reaction_time,IBI,WHALE):

    # Case Excel sheet
    csv_dir = str(path + '/' + folder + '/' + 'cases_file_' + folder + '.csv')
    header_list = read_csv_header(csv_dir)
    df = pd.read_csv(csv_dir, names=header_list, header=0)

    #Important parameters:
    ship_heights=st_to_array(pd.Series(df['ship height (m)']).array[-1])
    speeds=[st_to_array(pd.Series(df['ship speeds (m/s)']).array[-1])]

    #Variables needed for running code:
    av_probs_fd1 = {}
    std_probs_fd1 = {}
    names = []

    directory1 = path + folder + '/'
    for filename in os.listdir(directory1):
        if filename.endswith(".pickle"):# and filename.startswith('IBI'):
            object = pd.read_pickle(directory1 + filename)
            name = object['run name']
            names.append(name)
            av_probs_fd1[name] = object['Probs average of detection']
            std_probs_fd1[name] = object['Probs std of detection']
    detection = ['RDR', 'DDF']

    ##IBI
    if IBI==1:
        #  PLOTTING
        font = {'family' : 'sans-serif',
                'weight' : 'normal',
                'size'   : 20}
        plt.rc('font', **font)
        fig1, ax1 = plt.subplots(len(ship_heights),len(reaction_time), figsize=(15,18))
        color = ['indigo', 'darkviolet', 'mediumorchid', 'plum', 'darkgreen', 'forestgreen', 'limegreen', 'springgreen']


        for s in ship_heights:
            for rt in reaction_time:
                i_color=0
                subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(s)
                for d in detection:
                    for i in inter_blow:
                        dict1='IBI_'+str(i)+'_'+d+'_'+mode
                        info=av_probs_fd1[dict1][subdict]
                        row, column = row_column(rt, s,reaction_time,ship_heights)
                        line1, = ax1[row, column].plot(np.asarray(speeds).T, info, color=color[i_color],label='IBI:' + str(i)+','+d,**font)
                        i_color=i_color+1

                        #Grid
                        ax1[row,column].grid()

                        # axis ticks
                        if row != 4:
                            ax1[row, column].set_xticklabels([])
                        if column != 0:
                            ax1[row, column].set_yticklabels([])

                        # title
                        ax1[row, column].set_title('RT:' + str(int(rt / 60)) + 'min, MD=' + str(s) + 'm',**font)

                        # y axis:
                        ax1[row, 0].set(ylabel='ITDP',**font)
                        #ax1[row, 0].yaxis.get_label().set_fontsize(16)

                        # x axis:
                        ax1[4, column].set(xlabel='Ship speed (m/s)',**font)
                        #ax1[4, column].xaxis.get_label().set_fontsize(16)

        #Set y axis limits
        for ax in ax1.flat:
            ax.grid()
            ax.set_ylim(-0.05,1.05)

        # Turn off tick labels
        ax1[0, 0].set_xticklabels([])
        #ax1[0, 0].annotate('A', (1, 0), fontsize=30,)

        #Legend
        plt.subplots_adjust(right=0.8)
        ax1[4,1].legend(title='Legend:', bbox_to_anchor=(1.04,3.0), loc="center left", borderaxespad=0.,**font) #ncol=2

        #Second axis
        add_2axis(1, ax1[4, 0])
        add_2axis(1, ax1[4, 1])

        fig1.suptitle('MODE:'+mode+ '\n'+'from run: '+folder)
        #plt.tight_layout()

        plt.savefig(path+folder+'/MODE:'+mode+'.png')#,bbox_inches='tight')
        plt.show()

    if WHALE==1:
        whale_speeds=np.array([0,1,2,3])
        #  PLOTTING
        font = {'family' : 'sans-serif',
                'weight' : 'normal',
                'size'   : 20}
        plt.rc('font', **font)
        fig1, ax1 = plt.subplots(len(ship_heights),len(reaction_time), figsize=(15,18))
        color = ['indigo', 'blue', 'darkgreen','orange']


        for s in ship_heights:
            for rt in reaction_time:
                i_color=0
                subdict = 'reaction_time:' + str(rt) + 'ship_height:' + str(s)
                for wp in whale_speeds:
                    dict1='WhaleSpeed_'+str(wp)
                    info = av_probs_fd1[dict1][subdict]
                    row, column = row_column(rt, s,reaction_time,ship_heights)
                    line1, = ax1[row, column].plot(np.asarray(speeds).T, info, color=color[i_color],
                                                   label= str(wp)+'m/s')
                    i_color = i_color + 1

                   #Maybe from here : out of loop: common to IBI and whales
                    # Grid
                    ax1[row, column].grid()

                    # axis ticks
                    if row != 4:
                        ax1[row, column].set_xticklabels([],**font)
                    if column != 0:
                        ax1[row, column].set_yticklabels([],**font)

                    # title
                    ax1[row, column].set_title('RT:' + str(int(rt / 60)) + 'min, MD=' + str(s) + 'm', **font)

                    # y axis:
                    ax1[row, 0].set(ylabel='ITDP')
                    # ax1[row, 0].yaxis.get_label().set_fontsize(16)

                    # x axis:
                    ax1[4, column].set(xlabel='Ship speed (m/s)')
                    # ax1[4, column].xaxis.get_label().set_fontsize(16)

        # Set y axis limits
        for ax in ax1.flat:
            ax.grid()
            ax.set_ylim(-0.05, 1.05)

        # Legend
        plt.subplots_adjust(right=0.84)
        ax1[4, 1].legend(title='Whale Speed:', bbox_to_anchor=(1.04, 3.0), loc="center left",
                                 borderaxespad=0.)  # ncol=2

        # Second axis
        add_2axis(1, ax1[4, 0],font)
        add_2axis(1, ax1[4, 1],font)

        fig1.suptitle('Whale Speed Variations'+'\n'+ 'MODE:' + mode +',DDF, IBI:60S'  + '\n' + 'from run: ' + folder,**font)
                # plt.tight_layout()

        plt.savefig(path + folder + '/Whale_Speed_MODE' + mode + '.png')  # ,bbox_inches='tight')
        plt.show()


#RUN CODE HERE
#Inputs
prefix='/home/loicka/Desktop/ws_whorld/organized_whorld'
path=prefix+'/OUTPUTS/RUN_RESULTS/'
folder='June_7th_50ep'
mode = 'mixed'
# todo extract rt from excel sheet
reaction_time = np.array([60, 300])
inter_blow = np.array([15, 30, 60, 120])  # todo user input
ship_speed_vs_prob_plot(folder,path,mode,inter_blow,reaction_time, 0,1)