
def main_function(json_filename,output_destination):
    #LIBRAIRIES/FUNCTIONS
    # Libraries
    import numpy as np
    import pickle
    import sys
    import json
    import time
    from pytictoc import TicToc
    import datetime
    import csv
    import logging

    # Functions
    from CODE.functions import f_whale
    from CODE.functions import f_ship
    from CODE.functions import f_detection
    from CODE.functions import f_plots
    from CODE.functions import f_dive_profile
    from CODE.functions import f_info_for_dp
    #from CODE.functions import f_triage_repertoire_dp

    def st_to_array(string):
        li = list(string.split(","))
        li= [int(x) for x in li]
        array=np.asarray(li)
        return array

    # Data extraction
    data = json.load(open(json_filename)) #extract info from cases_file excel sheet
    epoch = int(data['epoch number']) # int
    time_run = int(data['run time (s)'])  # int
    width = int(data['grid width (m)']) *2 # int
    ship_height = st_to_array(data['ship height (m)']) # array
    ship_nb = int(data['ship number'])  # int
    ship_speeds = st_to_array(data['ship speeds (m/s)']) # np.array((#,))
    l=time_run*ship_speeds[-1]+(time_run*ship_speeds[-1]/10) #length of grid is proportional to max ship speed
    beta_ship = int(data['ship heading (deg)'])  # int
    angle_detection = int(data["angle of detection (deg)"])  # int
    if angle_detection == 0:
        sys.exit("Angle of detectable_whales_xyz must be >0 degree")
    DDF=int(data['data detection function'])
    ship_reaction_time = np.asarray([int(data['ship reaction time #1 (s)']),int(data['ship reaction time #2 (s)']),int(data['ship reaction time #3 (s)'])])  # array
    whale_nb = int(data["whale number"]) # int
    interval_blow = int(data["Interval btw blows (s)"])
    all_whales_blow = int(data["All whales blow"])
    all_whales_surf = int(data["All whales surface"])
    all_whales_sub= int(data["All whales subsurface"])
    all_whales_deep = int(data["All whales deep"])
    mean_v = float(data["mean whale velocity (m/s)"])
    std_v =float(data["std whale velocity (m/s)"])
    mode = data["dive profile mode"]  # str
    plt_probs = int(data['plot probabilities']) # bool
    plt_world = int(data['plot world']) # bool
    ETA_display=int(data['ETA display'])
    run_name=data['Case Description']

    ## Logging set up
    if ETA_display==1:
        LOG = output_destination+'/ETAlog_'+str(data["Case Description"])+'.log'
        logging.basicConfig(
            filename=LOG,
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        # set up logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # set a format which is simpler for console use
        formatter = logging.Formatter(' %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        logger = logging.getLogger(__name__)

    start_time = time.time()
    t = TicToc()

    # For detectatibility function
    possibleAngles,startAngle,endAngle=f_detection.make_sectorangles(beta_ship,angle_detection)

    prob_detection = {}

    detected_whales_xyz = {}
    indanger_whales_xyz = {}

    detected_ships_xy = {}
    indanger_ships_xy = {}

    # testing_vessel_log = []
    # radius_detect_log = []
    detection_probs_log = {}

    past=0

    if ETA_display==1:
        logging.info("Case #:"+ data["Case #"])
        #print('Case %s ...\n' % (run_name))

    vect1, vect2, vect3, two_one, two_three = f_info_for_dp.get_info_for_dp(mode)

    prob_average_final={}
    prob_std_final={}

    for num_iter in range(epoch):
        for r_time in ship_reaction_time:
            for ship_h in ship_height:  # for all ship heights

                detection_probs, detection_dist, radius_detect, testing_vessel=f_ship.extract_dist_data_poipu(ship_h)

                # Logging
                detection_probs_log.setdefault(ship_h, []).append(detection_probs)

                for v in range(np.size(ship_speeds)):# for all ship speeds
                    t.tic() #Start timer

                    speed1 = ship_speeds[v]
                    exclusion_distance = speed1 * r_time

                    # Whales x,y,z positions
                    whale_x, whale_y, whale_z = f_whale.whale_dict(time_run, whale_nb, l, width, mode,
                                                                      all_whales_blow, all_whales_surf,all_whales_sub,
                                                                      all_whales_deep, mean_v, std_v, interval_blow,vect1,
                                                                                        vect2, vect3, two_one, two_three)
                    # Ship x, y positions
                    ship_x, ship_y = f_ship.ship_dict(time_run, ship_nb, l, width, beta_ship, speed1)

                    name = 'epoch:' + str(num_iter) + 'reaction_time:' + str(r_time) + 'ship_height:' + str(
                        ship_h) + 'speed:' + str(speed1)

                    encounter_result=[]

                    # Detection function
                    for s in range(ship_nb):
                        for w in range(whale_nb):
                            score, detected_whale,detected_ship,indanger_whale,indanger_ship = \
                                f_detection.detection_function(whale_x[w], whale_y[w], whale_z[w], ship_x[s],
                                                                  ship_y[s], possibleAngles, exclusion_distance,DDF,detection_probs, detection_dist, radius_detect)

                            encounter_result = np.append(encounter_result, score)
                            if len(detected_whale)!=0:
                                detected_whales_xyz.setdefault(name, []).append(detected_whale)
                                detected_ships_xy.setdefault(name, []).append(detected_ship)
                            if len(indanger_whale)!=0:
                                indanger_whales_xyz.setdefault(name, []).append(indanger_whale)
                                indanger_ships_xy.setdefault(name, []).append(indanger_ship)

                    name_prob = 'reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h)+ 'speed:' + str(speed1)
                    if len(encounter_result)==0:
                        prob_detection_calc=np.nan
                    else:
                        prob_detection_calc = np.sum(encounter_result)/len(encounter_result)#sum/len
                    prob_detection.setdefault(name_prob, []).append(prob_detection_calc) #dictionary of lists

                    #ETA
                    time_current= t.tocvalue()
                    past=past+time_current
                    ETA=time_current*epoch*len(ship_reaction_time)*len(ship_height)*len(ship_speeds)-past
                    ts = time.time()
                    time_stamp=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %d/%m/%Y')
                    if ETA_display == 1:
                        logging.info('ETA: ' + str(int(ETA)) + 's or ' + str(round(ETA / 60, 2)) + 'min or ' + str(round(ETA / 3600, 2)) + ' hours at Epoch#' + str(num_iter) + ' at '+
                                     time_stamp)

        prob_average_epoch, prob_std_epoch = f_detection.get_final_prob_std(ship_reaction_time, ship_height,
                                                                          prob_detection)
        content = {
        "case #": data["Case #"],
        "run name": run_name,
        'epoch #': num_iter,
        "Probs average of detection": prob_average_epoch,
        "Probs std of detection": prob_std_epoch,
        "Probs detection": prob_detection,
        }
        pickle.dump(content, open(output_destination + '/epochs_folder/'+'epoch' +str(num_iter)+'_'+ run_name + '.pickle', "wb"))

    prob_average_final,prob_std_final= f_detection.get_final_prob_std(ship_reaction_time,ship_height,prob_detection)


    # PLOTTING
    if plt_probs == True:
        f_plots.probability_plt(ship_height,ship_speeds,prob_average_final,prob_std_final,ship_reaction_time,run_name,epoch,output_destination)

    if plt_world == True:
        f_plots.whorld_plt(ship_nb, ship_x, ship_y, beta_ship, angle_detection, time_run, startAngle, endAngle,
                       radius_detect, whale_nb,whale_x, whale_y, ship_reaction_time, width, l, epoch, ship_height,
                       indanger_whales_xyz, detected_whales_xyz, run_name, ship_speeds,output_destination)

    time_stamp=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %d/%m/%Y')
    #print('About to store... at '+time_stamp)
    if ETA_display==1:
        logging.info('About to store... at '+time_stamp)

    ###STORE VALUES INTO PICKLE FILE
    # with open("RUN_RESULTS/" + run_name, "wb") as f:
    content = {
        "case #": data["Case #"],
        "run name": data['Case Description'],  # str
        "Detection distance": detection_dist,
        "Detection probabilities": detection_probs_log,
        "Probs whale detection per speeds": prob_detection,
        "Probs average of detection": prob_average_final,
        "Probs std of detection": prob_std_final,
    }
    w = csv.writer(open(output_destination + '/' + run_name+'_average.csv', "w"))
    for key, val in prob_average_final.items():
        w.writerow([key, val])

    w1 = csv.writer(open(output_destination + '/' + run_name + '_std.csv', "w"))
    for key, val in prob_std_final.items():
        w1.writerow([key, val])

    pickle.dump(content, open(output_destination + '/' + run_name + '.pickle', "wb"))
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %d/%m/%Y')

    if ETA_display==1:
        logging.info('Output file directory:'+output_destination + '/' + run_name)
        logging.info('All stored at ' + time_stamp)

    time_exec=(time.time() - start_time)

    print('Execution time %s seconds, or %s minutes, or %s hours ' % (round(time_exec),round(time_exec/60,2),round(time_exec/3600,2)))
    if ETA_display==1:
        logging.info('Execution time %s seconds, or %s minutes, or %s hours ' % (round(time_exec),round(time_exec/60,2),round(time_exec/3600,2)))