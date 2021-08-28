
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script contains all the functions associated with whales' trajectory

'''
def whale_dict(time_run, w, l, width, mode, all_whales_blow, all_whales_surf, all_whales_sub,all_whales_deep,
               mean_v, std_v, interval_blow,vect1, vect2, vect3, two_one, two_three):
    """ This function computes the new x/y position of a ship for random speeds and angles
     :param time_run: iteration number/# of positions to compute (time step=1min)
     :param w: number of whales
     :return: new x and y positions
     :param ship_nb: length of grid lxl
     :return: new x,y,z whales' positions
    """
    import numpy as np
    import random
    from CODE.functions import f_dive_profile

    whale_x={}
    whale_y={}
    whale_z={}

    for w in range(w):
        #Store unique diving profile (z) for each whale

        dp= f_dive_profile.create_dive_profile(vect1, vect2, vect3, two_one, two_three, interval_blow)

        if all_whales_blow==True:
            whale_z[w] = np.full((time_run, 1), 0)
        elif all_whales_surf==True:
            whale_z[w] = np.full((time_run, 1), 1)
        elif all_whales_sub== True:
            whale_z[w] = np.full((time_run, 1), 2)
        elif all_whales_deep == True:
            whale_z[w] = np.full((time_run, 1), 3)
        else: #TRUE DP
            whale_z[w]= dp[0:time_run].reshape((time_run,1))
       #
        #Whales x/y positions
        wx= np.zeros((time_run, 1))
        wy= np.zeros((time_run, 1))

        # Random initial x,y positions
        wx[0,0]=random.randrange(width)
        wy[0,0]=random.randrange((15*120),l) #whales are positioned outside of max exclusion zone: max speed * max reaction time

        beta_whale_offset=random.randint(0, 360)
        for i in range(1, time_run):
            velocity=random.normalvariate(mean_v, std_v)
            # corrolated random walk w/ random component of +/- 5 for each time step
            beta_whale=beta_whale_offset+random.randrange(-5, 5, 1)
            #beta_whale=beta_whale_offset
            beta_whale_offset=beta_whale
            wx[i,0]=wx[i-1,0]+velocity*np.cos(np.deg2rad(beta_whale))
            wy[i,0]=wy[i-1,0]+velocity*np.sin(np.deg2rad(beta_whale))

        #Store positions in dictionaries
        whale_x[w]=wx
        whale_y[w]=wy

    return whale_x, whale_y, whale_z

