

#####STEPS
#1 Code created "updated" folder in desired location
#1 ALl files are copied and pickle files are updated
#Manually: Create "old folder" and move original files in it, move files in updated folder back out (main directory)
import os
import pickle
import pandas as pd
import shutil
# directory='/home/loicka/Desktop/ws_whorld/RESULTS_BIG_COMP/25_02_2021/'
# repertoire_raw=pd.read_pickle(directory+'ep10,rt3600,w100,s3,allblow:F,allsurf:F,allsub:F,alldeep:T,wmean_v:0,wstd_v:0,inter_blow:60,DDF:0,mode:mixed.pickle')

path='/home/loicka/Desktop/ws_whorld/RESULTS_BIG_COMP/'
folder1='June_7th_50ep'

directory1 = path + folder1 + '/'

 #create updated folder
os.mkdir(directory1+'updated')

# START
names = []
# FOLDER 1
# Variables needed for running code:
av_probs_fd1 = {}
std_probs_fd1 = {}
filenames = [ name for name in os.listdir(directory1) if not os.path.isdir(os.path.join(directory1, name)) ]
for filename in filenames:
    if filename.endswith(".pickle"):
        object = pd.read_pickle(directory1 + filename)
        if 'RDR' in object['run name']:
           object['run name']=object['run name'].replace('RDR', 'DDF')
        if 'MDR' in object['run name']:
           object['run name']=object['run name'].replace('MDR', 'RDR')
        pickle.dump(object,open(path+folder1+'/updated/' + filename, "wb"))
    else:
        original = directory1+filename
        target = directory1+'updated/'+filename
        shutil.copy(original,target)

