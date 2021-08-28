# Libraries
import os.path
import shutil
import glob
from multiprocessing import Pool
os.environ['QT_QPA_PLATFORM']='offscreen'
import pandas as pd

#Functions
from CODE.functions import f_main
from CODE.functions import f_csv_to_json

prefix='/home/loicka/Desktop/ws_whorld/organized_whorld'  #todo modify here

#Change current working directory
os.chdir(prefix)

#Create folder to dump results:
new_folder=input('SET TRIAL FOLDER NAME:')
output_destination=prefix+'/OUTPUTS/RUN_RESULTS/'+new_folder
os.mkdir(output_destination)

#REMOVE ALL PREVIOUS CASES
cases_file_path=prefix+'/CODE/scenario_runs/CASES_RUN/'
files = glob.glob(cases_file_path+'*')
for f in files:
    os.remove(f)

# RUN FUNCTION TO CREATE JSON CASE FILES
csvFilePath=prefix+'/CODE/scenario_runs/cases_short.csv' #todo change here
jsonFilePath=prefix+'/CODE/scenario_runs/CASES_RUN/'
f_csv_to_json.make_json(csvFilePath, jsonFilePath)

#Make copy of CSV file to new_folder
original =csvFilePath
target = output_destination+'/cases_file_'+new_folder+'.csv'
shutil.copy(original, target)

#CREATE INPUT FOR FUNCTION
#Counts number of json files -- i.e #cases
DIR = prefix+'/CODE/scenario_runs/CASES_RUN/'
number_cases=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
inputlist=[]

for i in range(1,number_cases+1):
    name=DIR+'case'+str(i)
    inputlist.append([name,output_destination])

#Create epoch folder as backup:
os.mkdir(output_destination+'/'+'epochs_folder')

#for i in range(1,number_cases+1):
#    print(inputlist[i])
#    f_main.main_function(inputlist[i][0],inputlist[i][1])

with Pool(processes=number_cases+1) as pool:
    for _ in pool.starmap(f_main.main_function,  inputlist):
        pass

#DELETE json files used for trial *double check
# REMOVE ALL PREVIOUS CASES
cases_file_path = prefix+'/CODE/scenario_runs/CASES_RUN/'
files = glob.glob(cases_file_path + '*')
for f in files:
    os.remove(f)



