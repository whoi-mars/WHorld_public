'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script contains all the functions associated with the implementation of detection of whales by ships.

'''
def detection_function(whale_x, whale_y, whale_z, ship_x, ship_y, possibleAngles, exclusion_distance,DDF,detection_probs, detection_dist, radius_detect):
    import numpy as np
    #WORKS!

    score = []
    detected_whale = []
    detected_ship = []
    indanger_whale = []
    indanger_ship = []
    detected_log = []

    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    dist_w_s = np.sqrt(((delta_x ** 2) + (delta_y ** 2)))
    angle_w_s = np.round(((np.arctan2(delta_y, delta_x)) * 180 / np.pi) % 360, 1)

    in_ex=np.where(np.logical_and(np.greater_equal(exclusion_distance,dist_w_s),np.greater_equal(dist_w_s,0)))[0] # >=exclusion_zone=>dist_w_s>0
    vuln_sector=np.where(np.logical_and(np.not_equal(whale_z,3),np.in1d(angle_w_s,possibleAngles)))[0] #state 012+in sector angles
    in_ex_vuln=np.intersect1d(in_ex, vuln_sector) # exclusion zone angles + state 012

    if len(in_ex_vuln)!=0:
        if DDF==0:
            in_dz= np.where(np.logical_and(np.greater(dist_w_s,exclusion_distance), np.greater_equal(radius_detect,dist_w_s)))[0] #radius_detect>=dist_ws>exclusion_zone
        else:
            out_ex=np.where(dist_w_s>exclusion_distance)[0]
            for i in out_ex:
                p=get_prob_from_dist(int(dist_w_s[i]),detection_probs, detection_dist, radius_detect,DDF)
                detected_value = np.random.binomial(1, p)
                detected_log=np.append(detected_log,detected_value)

            index_detected=np.where(detected_log==1)[0]
            in_dz=out_ex[index_detected]

        blowing_sector=np.where(np.logical_and(np.equal(whale_z,0),np.in1d(angle_w_s,possibleAngles)))[0] #blowing+in sector angles
        in_dz_blowing = np.intersect1d(in_dz, blowing_sector) #blowing in dz

        if len(in_dz_blowing)!=0:
            score=1
            detected_whale=np.array((whale_x[in_dz_blowing][0],whale_y[in_dz_blowing][0],whale_z[in_dz_blowing][0]))
            detected_ship=np.array((ship_x[in_dz_blowing][0],ship_y[in_dz_blowing][0]))
        else:
            score=0
            indanger_whale = np.array((whale_x[in_ex_vuln][0], whale_y[in_ex_vuln][0], whale_z[in_ex_vuln][0]))
            indanger_ship = np.array((ship_x[in_ex_vuln][0], ship_y[in_ex_vuln][0]))

    return score, detected_whale,detected_ship,indanger_whale,indanger_ship


def make_sectorangles(beta_ship,angle_detection):
    import numpy as np

    startAngle = (beta_ship - angle_detection / 2)
    endAngle = (beta_ship + angle_detection / 2)
    if startAngle < 0:
        startAngle = startAngle % 360
        pA = np.arange(startAngle, 360, 0.1)
        pB = np.arange(0, endAngle, 0.1)
        possibleAngles = np.round(np.sort(np.append(pA, pB)), 1)
    else:
        possibleAngles = np.round(np.arange(startAngle, endAngle+0.1, 0.1), 1)

    return possibleAngles,startAngle,endAngle

def get_prob_from_dist(dist,detection_probs, detection_dist, radius_detect,DDF):
    import numpy as np

    dist=round(dist,-2) #round to nearest 100
    prob=[]

    if dist>=10000:
        prob=0
    if dist<=radius_detect:
        prob=1
    if dist>radius_detect:
            if DDF==0:
                prob=0
            else:
                min_index=np.argmin(abs(dist-detection_dist))
                prob=float(detection_probs[min_index])
    return prob


def get_final_prob_std(ship_reaction_time,ship_height,prob_detection):
    import numpy as np
    probs_average = {}
    probs_std = {}

    for k, v in prob_detection.items():
        # v is the list of probs for speed k
        probs_average[k] = np.nanmean(v)
        probs_std[k] = np.nanstd(v)

    # Transforms probabilities dictionaries into arrays of length= # of speeds
    prob_average_final = {}
    prob_std_final = {}
    for r_time in ship_reaction_time:
        for ship_h in ship_height:
            new_average = {k: v for k, v in probs_average.items() if
                           k.startswith('reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h))}
            prob_average_final['reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h)] = np.array(
                list(new_average.values()))

            new_std = {k: v for k, v in probs_std.items() if
                       k.startswith('reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h))}
            prob_std_final['reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h)] = np.array(
                list(new_std.values()))
    return prob_average_final,prob_std_final

