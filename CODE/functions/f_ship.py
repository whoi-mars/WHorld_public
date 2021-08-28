'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script contains all the functions associated with ship features: create/record trajectories, DDF detection curve (POIPU)

'''

def ship_dict(time_run, ship_nb, l,w, beta_ship, speed):
    #USED IN main_function.py
    import numpy as np
    import random

    ship_x = {}
    ship_y = {}
    for s in range(0, ship_nb):
        x = random.randrange(w)  # x0 position
        y = 0#random.randrange(0,int(l/100))  # y0 position
        x_end = (x + speed * np.cos(np.deg2rad(beta_ship)) * time_run) #end X position after time_run seconds
        y_end = (y + speed * np.sin(np.deg2rad(beta_ship)) * time_run) #end Y position after time_run seconds
        if y_end>l:
            t_l=int((l-y)/(speed * np.sin(np.deg2rad(beta_ship))))

            y_endNaN=np.zeros(((time_run-t_l)))
            y_endNaN[:]=np.nan

            x_endtrue = int((x + speed * np.cos(np.deg2rad(beta_ship)) * t_l)) #wont change from initial if beta_ship=90
            x_endNaN=np.zeros(((time_run-t_l)))
            x_endNaN[:]=np.nan

            ship_y[s]= np.concatenate((np.linspace(y,l,num=t_l,endpoint=True),y_endNaN[:,]),axis=0).reshape((time_run,1))
            ship_x[s] = np.concatenate((np.linspace(x, x_endtrue, num=t_l, endpoint=True),x_endNaN[:,]),axis=0).reshape((time_run,1))
        else:
            ship_x[s] = np.linspace(x, x_end, num=time_run, endpoint=True).reshape(time_run, 1)
            ship_y[s] = np.linspace(y, y_end, num=time_run, endpoint=True).reshape(time_run, 1)

    return ship_x, ship_y


def extract_dist_data_poipu(limit):
    import sys
    import pickle
    import os
    distributions_poipu= pickle.load(open(os.getcwd()+'/DATA/IR_data/distributions_poipu', "rb"))
    detection_dist=distributions_poipu['distances']
    detection_probs=distributions_poipu['probs_'+str(limit)]
    radius_detect=limit
    testing_vessel='DDF='+str(limit)

    return detection_probs,detection_dist,radius_detect,testing_vessel
#
# #FOR TESTING ONLY
# import numpy as np
# import matplotlib.pyplot as plt
# import random
# time_run=5000
# ship_nb=10
# l=10000
# beta_ship=90#random.randrange(0, 180, 1)
# ship_speeds=2
# radius_detect=100
#
# ship_x,ship_y=ship_dict(time_run, ship_nb, l, beta_ship,ship_speeds)
#
# for ship_nb in range(0,ship_nb):
#     plt.plot(ship_x[ship_nb],ship_y[ship_nb])
