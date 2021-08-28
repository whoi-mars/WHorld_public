'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SCRIPT focuses on using collected Thermal Imaging (IR) data
1. Import data from text files
2. Plot data as histograms
3. Fit log function to histogram to get approximated fit
4. From fitted log function, obtain max of curve (distance occurring the most: x_max,y_max)
5. Distribution function: : 0-x_max: y=1, x_max-end : y= log function

Note: WORKS!
'''

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import lognorm
import pickle
import operator
import csv


prefix='/home/loicka/Desktop/ws_whorld3'

distributions={}
x_max_log={}
font = {'family': 'sans-serif',
        'weight': 'normal',
        'size': 20}
#create subplots
fig, axs = plt.subplots(6,2, figsize=(20, 20), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.001)
axs = axs.ravel()
fig.tight_layout()

#Extract IR DATA
c=0
directory=prefix+'/DATA/IR_data/'
for filename in os.listdir(directory):
    if filename.endswith(".txt"):

#%% PRE-PROCESSING
        #Read txt data (string)
        data=open(directory+ filename, "r").read()
        print(filename)
        #separate Data at commas to make it a list of string
        if ',' in data:
            data=data.split(',')
        else:
            data=data.split('\n')[:-1]

        # Convert list into array of floats
        data = np.array(data).astype(float)
        #Remove NaN values
        data=data[~np.isnan(data)]
        np.savetxt(directory+'/cleaned_data/'+ filename, data, delimiter=',')

# HISTOGRAMS
        density_choice=True
        log_choice=False
        hist_color='skyblue'

        bins = np.arange(0, 10100,100)
        axs[c].hist(data, bins=bins, density=density_choice, log=log_choice,  label='Raw data', color=hist_color)
        plt.xlabel('Distance (m)')
        plt.ylabel('Density')

        # Find bin with highest frequency
        n, b, patches = plt.hist(data, bins, density=density_choice, log=log_choice, color=hist_color)
         # n: the number of counts in each bin of histograms
         # b: the left hand egde of each bin
         # patches: the ind. patches used to create histograms , eg: the collection of rectangles

        bin_max = np.argmax(n)
        axs[c].patches[bin_max].set_facecolor('plum')

        axs[c].plot(b[bin_max], n[bin_max], 'or',label='Max Bin (%.f,%.2e)' % (b[bin_max], n[bin_max]))

        # Log fit (pdf)
        shape, loc, scale = lognorm.fit(data,loc=0)
        x_pdf =  bins
        y_pdf = lognorm.pdf(x_pdf, shape, loc, scale) #(100,1)
        axs[c].plot(x_pdf, y_pdf, 'r', label='log pdf')

        # Max of log fit (pdf)
        y_max_pdf=max(y_pdf)
        x_max_indx=np.argmax(y_pdf)
        x_max_pdf=x_pdf[x_max_indx] #x values corresponding to max(pdf)
        x_max_log[filename]=x_max_pdf

        axs[c].plot(x_max_pdf,y_max_pdf,'*b', label='Max Log(%.f,%.2e)'%(x_max_pdf,y_max_pdf))
        axs[c].legend()

        c=c+1

#PROBS FUNCTION
        #plt.subplot(5, 2, c)
        y_pdf=y_pdf/max(y_pdf)
        y_pdf[:x_max_indx+1]=1

        axs[c].plot(bins, y_pdf)
        axs[c].plot(x_max_pdf, 1, '*b', label='x=%.f (m)' % x_max_pdf)
        axs[c].legend()
        c=c+1

        #Storing for distributions
        distributions['x_values']= x_pdf #can be overwritten bc same for all files
        distributions[filename]= y_pdf   # prob. distributions

    # #Store probability function
    distributions['max_distance']=x_max_log  #store x_max_pdf values of 5 files

#SUBPLOT FORMATTING

cols = ['Histograms', 'Distributions']
#rows = ['Cap Race: All','Princeville','Cape Race: Day','Cape Race: Night','Poipu']
rows= [f for f in os.listdir(directory) if f.endswith(".txt")]

pad = 5 # in points

for ax, col in zip(axs[:], cols):
    ax.annotate(col, xy=(0.5, 1), xytext=(0, pad),
                xycoords='axes fraction', textcoords='offset points',
                size='large', ha='center', va='baseline')

for ax, row in zip(axs[[0,2,4,6,8,10]], rows):
    ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                xycoords=ax.yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
#X LABEL
for ax in axs[-2:]:
    ax.set_xlabel('Distance (m)')

# Y LABEL
axs[-2].set_ylabel('Density')
axs[-1].set_ylabel('Probability')

fig.tight_layout()
fig.subplots_adjust(left=0.15, top=0.95)
plt.show()

#Save into pickle file
#pickle.dump(distributions, open("IR_data/files_created/distributions_values", "wb"))

#Plot of distributions
plt.plot(distributions['x_values'],distributions['IR_DF_caperace_day.txt'],label='Caperace_day (26m)')
plt.plot(distributions['x_values'],distributions['IR_DF_caperace_night.txt'],label='Caperace_night (26m)')
plt.plot(distributions['x_values'],distributions['IR_DF_Princeville.txt'],label='Princeville (49.8m)')
plt.plot(distributions['x_values'],distributions['IR_DF_Poipu.txt'],label='Poipu (16m)')
plt.plot(distributions['x_values'],distributions['TNG2020_data.txt'],label='TNG (5.5m)')

plt.title('Probs of Detections vs. Distance')
plt.xlabel('Distance (m)')
plt.ylabel('Probability of detection')
plt.grid()
plt.legend(loc='best')
plt.show()


#Plot of heights vs. range
heights=np.array([26,49.8,26,26,16,5.5])
sites=['CR_all','Princeville','CR_day','CR_night','Poipu','TNG']

#Sort heights and corresponding x_pdf_max distances
L = sorted(zip(heights, sites,np.asarray(list(distributions['max_distance'].values()))), key=operator.itemgetter(0))
ordered_heights, ordered_sites,ordered_x_max= zip(*L)
log_ord_heights=np.log(ordered_heights)
# print(heights,distributions['max_distance_prob1'])
# print(ordered_heights, ordered_sites, ordered_x_max)

plt.plot(log_ord_heights,ordered_x_max, 'bo')
plt.title('Range vs. heights')
plt.xscale('log')
plt.xlabel('Log(Heights)(m)')
plt.ylabel('Range (m)')

for i in range(0,len(np.array(heights))):
        plt.annotate(ordered_sites[i],(np.array(log_ord_heights[i]),np.array(ordered_x_max[i])))

plt.show()


#Ship heights:
# Poipu: 16 m
# Princeville: 49.8 m
# Cape Race: 26 m
#TNG: 5.5m


## POIPU FOCUSED ####
#PROCESSING
poipu_data=open(prefix+'/DATA/IR_data/cleaned_data/'+ 'IR_DF_Poipu.txt', "r").read()
if ',' in poipu_data:
    poipu_data = poipu_data.split(',')
else:
    poipu_data = poipu_data.split('\n')[:-1]
poipu_data = np.array(poipu_data).astype(float)

#TNG
#PROCESSING
tng_data=open(prefix+'/DATA/IR_data/cleaned_data/'+ 'TNG2020_data.txt', "r").read()
if ',' in tng_data:
    tng_data = tng_data.split(',')
else:
    tng_data = tng_data.split('\n')[:-1]
tng_data = np.array(tng_data).astype(float)

# Log fit (pdf)
shape, loc, scale = lognorm.fit(tng_data, loc=0)
x_pdf = bins
y_pdf_tng = lognorm.pdf(x_pdf, shape, loc, scale)  # (100,1)
y_max_indx_tng=np.argmax(y_pdf_tng)
y_pdf_slope_tng=(y_pdf_tng/max(y_pdf_tng))[y_max_indx_tng:]

#EXTRACT KNOWN DATA
distance_val=distributions['x_values']
probs_poipu_original=distributions['IR_DF_Poipu.txt']

## HISTOGRAMS
density_choice = True
log_choice = False
hist_color = 'skyblue'

fig1, ax1 = plt.subplots()

bins = np.arange(0, 10100, 100)
ax1.hist(poipu_data, bins=bins, density=density_choice, log=log_choice, label='Raw data', color=hist_color)
ax1.set_xlabel('Distance (m)')
ax1.set_ylabel('Density')

# Find bin with highest frequency
n, b, patches = plt.hist(poipu_data, bins, density=density_choice, log=log_choice, color=hist_color)
# n: the number of counts in each bin of histograms
# b: the left hand egde of each bin
# patches: the ind. patches used to create histograms , eg: the collection of rectangles

bin_max = np.argmax(n)
ax1.patches[bin_max].set_facecolor('plum')

ax1.plot(b[bin_max], n[bin_max], 'or', label='Max Bin (%.f,%.2e)' % (b[bin_max], n[bin_max]))

# Log fit (pdf)
shape, loc, scale = lognorm.fit(poipu_data, loc=0)
x_pdf = bins
y_pdf = lognorm.pdf(x_pdf, shape, loc, scale)  # (100,1)
ax1.plot(x_pdf, y_pdf, 'r', label='log pdf')

# Max of log fit (pdf)
y_max_pdf = max(y_pdf)
x_max_indx = np.argmax(y_pdf)
x_max_pdf = x_pdf[x_max_indx]  # x values corresponding to max(pdf)

ax1.plot(x_max_pdf, y_max_pdf, '*b', label='Max Log (%.f,%.2e)' % (x_max_pdf, y_max_pdf))
ax1.legend()
ax1.set_title('POIPU')
ax1.grid()
plt.show()

## PROB FUNCTIONS
distributions_poipu={}
distributions_poipu['distances']=distance_val

limits=np.array((500,1000,1500,2000,2500,3000))
fig2, axs2 = plt.subplots((len(limits)+1),1, figsize=(10, 20), facecolor='w', edgecolor='k')
fig3, axs3 = plt.subplots(1,1, figsize=(10, 10), facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace = .5, wspace=.001)
axs2 = axs2.ravel()
fig2.tight_layout()

#ORIGINAL:MAX 1900m
distributions_poipu['probs_orignal_'+str(x_max_pdf)]=probs_poipu_original
axs2[0].plot(distance_val, probs_poipu_original)
axs2[0].plot(x_max_pdf, 1, '*b', label='x=%.f (m) (Original)' % x_max_pdf)
axs2[0].legend()
axs2[0].grid()

y_max_indx=np.argmax(y_pdf)
y_pdf_slope=(y_pdf/max(y_pdf))[y_max_indx:]
color=['black','darkmagenta','plum','navy','teal','darkgreen','saddlebrown']
linestyles=['solid','solid','dashed','dashdot','dotted', (0, (3, 1, 1, 1)),(0, (3, 5, 1, 5, 1, 5))]
i=1
for limit in limits:
    length=int(limit/100)
    y_pdf_1s=np.full((length,),1)
    y_pdf_goal=np.append(y_pdf_1s,y_pdf_slope)[0:len(distance_val)]
    y_pdf_goal_tng=np.append(y_pdf_1s,y_pdf_slope_tng)[0:len(distance_val)]
    if length < y_max_indx:
        l2=abs(length-y_max_indx)
        y_pdf_0s = np.full((l2,), 0)
        y_pdf_goal = np.append(y_pdf_goal, y_pdf_0s)[0:len(distance_val)]
        y_pdf_goal_tng = np.append(y_pdf_goal_tng, y_pdf_0s)[0:len(distance_val)]

    DDF=np.append(np.full((length+1,),1),np.full((100-length,),0))
    DDF1=np.append(np.full((limit,),1),np.full((10000-limit,),0))
    axs2[i].plot(DDF1,label='RDR',color='indigo')
    #axs2[i].plot(distance_val, y_pdf_goal_tng, label='TNG', color='blue')
    axs2[i].plot(distance_val, y_pdf_goal, label='DDF',color=color[i])
    axs3.plot(distance_val,y_pdf_goal,label=str(limit)+'m',color=color[i],ls=linestyles[i])
    axs2[i].plot(limit, 1, '*b', label='Detection Range=%.f (m)' % limit)
    axs2[-1].set_xlabel('Distance (m)')
    axs2[i].set_ylabel('Probability')
    axs2[i].legend()
    axs2[i].grid()
    #LOGGING
    distributions_poipu['probs_'+str(limit)]=y_pdf_goal
    i=i+1
axs3.set_xlabel('Distance (m)',**font)
axs3.set_ylabel('Detection Probability',**font)
axs3.legend(title='Detection range:')
axs3.grid()

plt.tight_layout()
plt.show()

#%% 1x2 SUBPLOT
font = {'family': 'sans-serif',
        'weight': 'normal',
        'size': 13}

fig5,((ax5,ax55))=plt.subplots(ncols=2,nrows=1,figsize=(12,5))

## HISTOGRAMS
density_choice = True
log_choice = False
hist_color = 'skyblue'

bins = np.arange(0, 10100, 100)
ax5.hist(poipu_data, bins=bins, density=density_choice, log=log_choice, label='Raw data', color=hist_color)
ax5.set_xlabel('Distance (m)',**font)
ax5.set_ylabel('Density',**font)

# Find bin with highest frequency
n, b, patches = plt.hist(poipu_data, bins, density=density_choice, log=log_choice, color=hist_color)
# n: the number of counts in each bin of histograms
# b: the left hand egde of each bin
# patches: the ind. patches used to create histograms , eg: the collection of rectangles

bin_max = np.argmax(n)
#ax5.patches[bin_max].set_facecolor('plum')

#ax5.plot(b[bin_max], n[bin_max], 'or', label='Max Bin (%.f,%.2e)' % (b[bin_max], n[bin_max]))

# Log fit (pdf)
shape, loc, scale = lognorm.fit(poipu_data, loc=0)
x_pdf = bins
y_pdf = lognorm.pdf(x_pdf, shape, loc, scale)  # (100,1)
ax5.plot(x_pdf, y_pdf, 'r', label='log pdf')

# Max of log fit (pdf)
y_max_pdf = max(y_pdf)
x_max_indx = np.argmax(y_pdf)
x_max_pdf = x_pdf[x_max_indx]  # x values corresponding to max(pdf)

ax5.plot(x_max_pdf, y_max_pdf, '*b', label='Max Log (%.f m)' % (x_max_pdf))
ax5.legend()
#ax5.set_title('POIPU',**font)
ax5.grid()

#AX55
#ORIGINAL:MAX 1600m
limit=1600
length = int(limit / 100)
DDF = np.append(np.full((length + 1,), 1), np.full((100 - length,), 0))
DDF1 = np.append(np.full((limit,), 1), np.full((10000 - limit,), 0))
ax55.plot(DDF1, label='RDR', color='indigo')
distributions_poipu['probs_orignal_'+str(x_max_pdf)]=probs_poipu_original
ax55.plot(distance_val, probs_poipu_original, label='DDF',color='darkgreen')
ax55.plot(x_max_pdf, 1, '*b', label='x=%.f (m) (POIPU Original)' % x_max_pdf)
ax55.set_xlabel('Distance (m)',**font)
ax55.set_ylabel('Detection Probability',**font)
ax55.legend()
ax55.grid()
plt.show()