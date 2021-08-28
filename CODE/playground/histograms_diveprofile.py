
#PLOTS ARTIFICIAL DP
#MAKE MANY (50 NOW) PLOTS OF ARTIFICIAL DP AND CORRESPONDING HISTOGRAMS

import numpy as np
from CODE.functions import f_dive_profile
import matplotlib.pyplot as plt


def occurences_count(vector):
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


mode='shallow'
vec_1, vec_2, vec_3, two_one, two_three = f_dive_profile.info_for_dp_funct(mode)


interval_blow=60
number_plot=50

# fig, axs = plt.subplots(number_plot,2, figsize=(80, 20), facecolor='w', edgecolor='k')
# fig.subplots_adjust(hspace = .5, wspace=.001)
#axs = axs.ravel()

fig = plt.figure(figsize=(20, 80), facecolor='w', edgecolor='k')
fig.tight_layout()
fig.subplots_adjust(hspace = .75)
gs0 = fig.add_gridspec(number_plot, 2)


c=0
for i in range(number_plot):
    #plot dive profile
    dp= f_dive_profile.create_dive_profile2(vec_1, vec_2, vec_3, two_one, two_three, interval_blow)
    vect0,vect1,vect2,vect3=occurences_count(dp)

    #DIVE PROFILE
    ax1 = fig.add_subplot(gs0[c])
    ax1.plot((-1)*dp[0:5000])
    ax1.set_ylabel('States')
    ax1.set_xlabel('Time (s)')

    #HISTO
    bins = np.arange(0, 150, 5)
    gssub = gs0[c+1].subgridspec(1, 4)
    for i in range(4):
        ax2=fig.add_subplot(gssub[0, i])
        if i==0:
            ax2.hist(vect0,bins)
            ax2.set_title('vect 0')
        elif i==1:
            ax2.hist(vect1,bins)
            ax2.set_title('vect 1')
        elif i == 2:
            ax2.hist(vect2, bins)
            ax2.set_title('vect 2')
        elif i == 3:
            ax2.hist(vect3, bins)
            ax2.set_title('vect 3')

        ax2.set_ylabel('Density')
    c = c + 2

    #ax1.set_suptitle('Dive profile')

plt.title(mode)
plt.text(500,200,'Artificial dive profile & corresponding Histograms', horizontalalignment='center',verticalalignment='center',fontsize=12)
plt.show()
