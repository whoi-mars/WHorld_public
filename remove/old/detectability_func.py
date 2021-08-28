
def detectability_2(radius_detect, xw, yw, zw, xs, ys, startAngle, endAngle, detection, surface, subsurface, speed, plot):
    """
         :param xs,ys: ship positions
         :param xw,yw,zw: whale positions
         startAngle: from FOV function
         endEngle: from FOV function
         radius_detect= radius of detectable_whales_xyz (m)
         xw,yw,zw: whale positions
         xs,ys: ship positions
         detectable_whales_xyz: if vulnerable_whales_xyz+ 2min far away from ship
         ship_speeds: ship ship_speeds
         vulnerable_whales_xyz: when whale is detected (in radius) at vulnerable_whales_xyz
         vulnerable_whales_xyz: whale is detected (in radius), within 10m of vulnerable_whales_xyz (in both exclusion and out of exclusion zones)
         detectable_whales_xyz: whale is detected at vulnerable_whales_xyz, out of exclusion zone
         """
    import numpy as np
    import math

    delta_x = xw - xs
    delta_y = yw - ys
    dist_w_s = (np.sqrt(((delta_x ** 2) + (delta_y ** 2))))
    detected = 0

    if dist_w_s>radius_detect:
        detected=0
    else:
        angle_w_s = round((math.degrees(math.acos(delta_x / dist_w_s))))
        exclusion_distance = speed * (2 * 60)  # 2min
        if delta_y < 0:
            angle_w_s = (-1) * angle_w_s

        if angle_w_s < 0:
            angle_w_s = angle_w_s % 360  # takes modulus, same as angle+360

        if startAngle > endAngle:
            pA = np.arange(startAngle, 361, 1)
            pB = np.arange(0, endAngle + 1, 1)
            possible_angles = np.sort(np.append(pA, pB))
        else:
            possible_angles = np.arange(startAngle, endAngle + 1, 1)

        if angle_w_s in possible_angles and dist_w_s <= radius_detect:
            if int(zw) == 0:  # at vulnerable_whales_xyz
                surface = np.vstack((surface, [xw, yw, zw]))
                detected = 1
                if dist_w_s > exclusion_distance and dist_w_s < radius_detect:  # whale is in "in time detectable_whales_xyz zone+ at vulnerable_whales_xyz"
                    detection = np.vstack((detection, [xw, yw, zw]))
            elif int(zw) == 1:  # below vulnerable_whales_xyz
                subsurface = np.vstack((subsurface, [xw, yw, zw]))
                detected = 1

        if plot==1:
            import matplotlib.pyplot as plt
            # for plotting sector lines
            # starting angle line
            startpt_x = np.cos(np.deg2rad(startAngle)) * radius_detect
            startpt_y = np.sin(np.deg2rad(startAngle)) * radius_detect
            # ending angle line
            endpt_x = np.cos(np.deg2rad(endAngle)) * radius_detect
            endpt_y = np.sin(np.deg2rad(endAngle)) * radius_detect
            plt.plot(xw, yw, 'y*',label='whale')  # plot whale position
            plt.plot(xs, ys, 'radius_detect*',label='ship')  # plot ship position
            plt.plot(startpt_x,startpt_y, 'c<', label='start Angle pt') #start angle logo
            plt.plot(endpt_x,endpt_y, 'm>', label='End Angle pt') #end angle logo
            plt.plot([0, startpt_x, 0, endpt_x], [0, startpt_y, 0, endpt_y],label='sector lines') # plot sector lines

            if np.size(detection, 0) != 1:
                plt.plot(detection[1:, 0], detection[1:, 1], "ro", label="In zone: Surface/Outside Exclusion zone (%d)"
                                                                         % (np.size(detection, 0) - 1))
            # ##At vulnerable_whales_xyz
            if np.size(surface, 0) != 1:
                plt.plot(surface[1:, 0], surface[1:, 1], "go", label="In zone: At vulnerable_whales_xyz (%d)" % (np.size(surface, 0) - 1))

            ## Under vulnerable_whales_xyz
            if np.size(subsurface, 0) != 1:
                plt.plot(subsurface[1:, 0], subsurface[1:, 1], "yo",
                         label="In zone: Under vulnerable_whales_xyz (%d)" % (np.size(subsurface, 0) - 1))

            plt.legend()
    return detection,surface,subsurface,detected

# # # ##TESTING CODE
# import numpy as np
#
# detectable_whales_xyz = np.zeros((1, 3))
# vulnerable_whales_xyz = np.zeros((1, 3))
# vulnerable_whales_xyz = np.zeros((1, 3))
# beta_ship=57
# angle=20
# startAngle = (beta_ship - angle / 2)   # take modulus
# endAngle = (beta_ship + angle / 2) % 360  # take modulus
#
# radius_detect=1000
# xs,ys=0,0
# xw,yw,zw=500,50,0
# ship_speeds=1
# a,b,c,d=detectability_2(radius_detect, xw, yw, zw, xs, ys, startAngle, endAngle, detectable_whales_xyz, vulnerable_whales_xyz, vulnerable_whales_xyz,ship_speeds,0)
#

#
def detectability(radius_detect, in_range_wx, in_range_wy,
                    in_range_wz, in_range_sx, in_range_sy,angle_w_s, dist_w_s, possibleAngles,
                  detection_whales_xyz,detection_ships_xy,
                  surface_whales_xyz,surface_ships_xy,
                  subsurface_whales_xyz,subsurface_ships_xy, speed, exclusion_distance, plot):
    """
         :param xs,ys: ship positions
         :param xw,yw,zw: whale positions
         startAngle: from FOV function
         endEngle: from FOV function
         radius_detect= radius of detectable_whales_xyz (m)
         xw,yw,zw: whale positions
         xs,ys: ship positions
         detectable_whales_xyz: if vulnerable_whales_xyz+ 2min far away from ship
         ship_speeds: ship ship_speeds
         vulnerable_whales_xyz: when whale is detected (in radius) at vulnerable_whales_xyz
         vulnerable_whales_xyz: whale is detected (in radius), within 10m of vulnerable_whales_xyz (in both exclusion and out of exclusion zones)
         detectable_whales_xyz: whale is detected at vulnerable_whales_xyz, out of exclusion zone
         """
    import numpy as np
    for i in range(len(angle_w_s)):
        if angle_w_s[i] in possibleAngles:  # and dist_w_s <= radius_detect:
            if int(in_range_wz[i]) == 0:  # at vulnerable_whales_xyz
                surface_whales_xyz = np.vstack((surface_whales_xyz, [int(in_range_wx[i]), int(in_range_wy[i]), int(in_range_wz[i])]))
                surface_ships_xy = np.vstack((surface_ships_xy, [int(in_range_sx[i]), int(in_range_sy[i])]))
                if dist_w_s[i] > exclusion_distance:  # whale is in "in-time detectable_whales_xyz zone + at vulnerable_whales_xyz"
                    detection_whales_xyz = np.vstack((detection_whales_xyz, [int(in_range_wx[i]), int(in_range_wy[i]), int(in_range_wz[i])]))
                    detection_ships_xy = np.vstack((detection_ships_xy, [int(in_range_sx[i]), int(in_range_sy[i])]))
                break
            elif int(in_range_wz[i]) == 1:  # below vulnerable_whales_xyz
                subsurface_whales_xyz = np.vstack((subsurface_whales_xyz, [int(in_range_wx[i]), int(in_range_wy[i]), int(in_range_wz[i])]))
                subsurface_ships_xy = np.vstack((subsurface_ships_xy, [int(in_range_sx[i]), int(in_range_sy[i])]))
                break
    return detection_whales_xyz,detection_ships_xy, surface_whales_xyz,surface_ships_xy, subsurface_whales_xyz,subsurface_ships_xy

    def detectability(radius_detect, in_range_wx, in_range_wy,
                      in_range_wz, in_range_sx, in_range_sy, angle_w_s, dist_w_s, possibleAngles,
                      detection_whales_xyz, detection_ships_xy,
                      surface_whales_xyz, surface_ships_xy,
                      subsurface_whales_xyz, subsurface_ships_xy, speed, exclusion_distance, plot):
        """
             :param xs,ys: ship positions
             :param xw,yw,zw: whale positions
             startAngle: from FOV function
             endEngle: from FOV function
             radius_detect= radius of detectable_whales_xyz (m)
             xw,yw,zw: whale positions
             xs,ys: ship positions
             detectable_whales_xyz: if vulnerable_whales_xyz+ 2min far away from ship
             ship_speeds: ship ship_speeds
             vulnerable_whales_xyz: when whale is detected (in radius) at vulnerable_whales_xyz
             vulnerable_whales_xyz: whale is detected (in radius), within 10m of vulnerable_whales_xyz (in both exclusion and out of exclusion zones)
             detectable_whales_xyz: whale is detected at vulnerable_whales_xyz, out of exclusion zone
             """
        import numpy as np
        for i in range(len(angle_w_s)):
            if angle_w_s[i] in possibleAngles:  # and dist_w_s <= radius_detect:
                if int(in_range_wz[i]) == 0:  # at vulnerable_whales_xyz
                    surface_whales_xyz = np.vstack(
                        (surface_whales_xyz, [int(in_range_wx[i]), int(in_range_wy[i]), int(in_range_wz[i])]))
                    surface_ships_xy = np.vstack((surface_ships_xy, [int(in_range_sx[i]), int(in_range_sy[i])]))
                    if dist_w_s[
                        i] > exclusion_distance:  # whale is in "in-time detectable_whales_xyz zone + at vulnerable_whales_xyz"
                        detection_whales_xyz = np.vstack(
                            (detection_whales_xyz, [int(in_range_wx[i]), int(in_range_wy[i]), int(in_range_wz[i])]))
                        detection_ships_xy = np.vstack((detection_ships_xy, [int(in_range_sx[i]), int(in_range_sy[i])]))
                    break
                elif int(in_range_wz[i]) == 1:  # below vulnerable_whales_xyz
                    subsurface_whales_xyz = np.vstack(
                        (subsurface_whales_xyz, [int(in_range_wx[i]), int(in_range_wy[i]), int(in_range_wz[i])]))
                    subsurface_ships_xy = np.vstack((subsurface_ships_xy, [int(in_range_sx[i]), int(in_range_sy[i])]))
                    break
        return detection_whales_xyz, detection_ships_xy, surface_whales_xyz, surface_ships_xy, subsurface_whales_xyz, subsurface_ships_xy



def detectability3(whale_x,whale_y,whale_z,ship_x,ship_y,possibleAngles,detection_whales_xyz, detection_ships_xy,
                      surface_whales_xyz, surface_ships_xy,
                      subsurface_whales_xyz, subsurface_ships_xy, exclusion_distance,detection_probs, detection_dist):
    import numpy as np

    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    angle_w_s = np.round(((np.arctan2(delta_y, delta_x)) * 180 / np.pi) % 360, 1)
    indexes = np.where(angle_w_s == possibleAngles)[0]

    for i in indexes:
        dist_w_s = round((np.sqrt(((delta_x[i] ** 2) + (delta_y[i] ** 2))))[0],-1) #round distance w/s to nearest tenth :10/20/30...
        if dist_w_s<10000: #10000 based on distribution curve x cut off
            index_distance=int(np.where(detection_dist==dist_w_s)[0]) #get index of distance
            probability=detection_probs[index_distance] #associated probability for above distance
            detected_value = np.random.binomial(1, probability)

            if detected_value==1:
                if int(whale_z[i]) == 0:  # at surface
                    surface_whales_xyz = np.vstack((surface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                    surface_ships_xy = np.vstack((surface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                    if dist_w_s> exclusion_distance:  # whale is in "in-time detectable_whales_xyz zone + at vulnerable_whales_xyz"
                        detection_whales_xyz = np.vstack((detection_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                        detection_ships_xy = np.vstack((detection_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                    break
                elif int(whale_z[i]) == 1:  # below surface
                    subsurface_whales_xyz = np.vstack((subsurface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                    subsurface_ships_xy = np.vstack((subsurface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                    break
    return detection_whales_xyz, detection_ships_xy, surface_whales_xyz, surface_ships_xy, subsurface_whales_xyz, subsurface_ships_xy



def detectability4(whale_x,whale_y,whale_z,ship_x,ship_y,possibleAngles,detection_whales_xyz, detection_ships_xy,
                      surface_whales_xyz, surface_ships_xy,
                      subsurface_whales_xyz, subsurface_ships_xy, exclusion_distance,detection_probs, detection_dist):

    '''
   works! slightly faster than detectability5, angle= first triage, then distance
    '''
    import numpy as np

    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    angle_w_s = np.round(((np.arctan2(delta_y, delta_x)) * 180 / np.pi) % 360, 1)

    # Whales within angle sector
    indexes = np.where(angle_w_s == possibleAngles)[0]

    if len(indexes) !=0:
   # Whales within 10km and angle sector
        dist_w_s= np.round(np.sqrt(((delta_x[indexes] ** 2) + (delta_y[indexes] ** 2))),-1)

        indexes_dist_under10km=np.where(dist_w_s<=10000)[0]
        indexes = indexes[indexes_dist_under10km]

        dist_w_s1=dist_w_s[dist_w_s <=10000 ] # keep distances under 10000m


        index_distance = (dist_w_s1/10).astype(int) # because bins every 10m
        probability = detection_probs[index_distance]

        detected_value = np.random.binomial(1, probability)
        indexes_detected_1=np.where(detected_value==1)[0].T
        indexes = indexes[indexes_detected_1]

        c=0
        for i in indexes:
            if int(whale_z[i]) == 0:  # at surface
                surface_whales_xyz = np.vstack((surface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                surface_ships_xy = np.vstack((surface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                if dist_w_s[c] > exclusion_distance:  # whale is in "in-time detectable_whales_xyz zone + at vulnerable_whales_xyz"
                    detection_whales_xyz = np.vstack(
                        (detection_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                    detection_ships_xy = np.vstack((detection_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                c=c+1
                break
            elif int(whale_z[i]) == 1:  # below surface
                subsurface_whales_xyz = np.vstack(
                    (subsurface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                subsurface_ships_xy = np.vstack((subsurface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                c=c+1
                break
    return detection_whales_xyz, detection_ships_xy, surface_whales_xyz, surface_ships_xy, subsurface_whales_xyz, subsurface_ships_xy


def detectability5(whale_x,whale_y,whale_z,ship_x,ship_y,possibleAngles,detection_whales_xyz, detection_ships_xy,
                      surface_whales_xyz, surface_ships_xy,
                      subsurface_whales_xyz, subsurface_ships_xy, exclusion_distance,detection_probs, detection_dist):
    '''
      works! slightly slower than detectability4 bc compute angle and dist for ALL
       '''

    import numpy as np

    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    angle_w_s = np.round(((np.arctan2(delta_y, delta_x)) * 180 / np.pi) % 360, 1)
    dist_w_s = np.round(np.sqrt(((delta_x ** 2) + (delta_y** 2))), -1)

    # Whales within angle sector
    indexes_angle = np.where(angle_w_s==possibleAngles)[0]
    indexes_distances= np.where(dist_w_s<=10000)[0]
    indexes=np.intersect1d(indexes_angle, indexes_distances)

    if len(indexes) !=0:

        index_distance_prob= (dist_w_s[indexes]/10).astype(int) # because bins every 10m
        probability = detection_probs[index_distance_prob]

        detected_value = np.random.binomial(1, probability)
        indexes_detected_1=np.where(detected_value==1)[0].T
        indexes = indexes[indexes_detected_1]

        c=0
        for i in indexes:
            if int(whale_z[i]) == 0:  # at surface
                surface_whales_xyz = np.vstack((surface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                surface_ships_xy = np.vstack((surface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                if dist_w_s[c] > exclusion_distance:  # whale is in "in-time detectable_whales_xyz zone + at vulnerable_whales_xyz"
                    detection_whales_xyz = np.vstack(
                        (detection_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                    detection_ships_xy = np.vstack((detection_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                c=c+1
                break
            elif int(whale_z[i]) == 1:  # below surface
                subsurface_whales_xyz = np.vstack(
                    (subsurface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                subsurface_ships_xy = np.vstack((subsurface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                c=c+1
                break
    return detection_whales_xyz, detection_ships_xy, surface_whales_xyz, surface_ships_xy, subsurface_whales_xyz, subsurface_ships_xy


def detectability6(whale_x,whale_y,whale_z,ship_x,ship_y,possibleAngles,detection_whales_xyz, detection_ships_xy,
                      surface_whales_xyz, surface_ships_xy,
                      subsurface_whales_xyz, subsurface_ships_xy, exclusion_distance,detection_probs, detection_dist):

    '''
   works! slightly faster than detectability5: distance = fist triage, then angle
    '''
    import numpy as np

    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    dist_w_s = np.round(np.sqrt(((delta_x ** 2) + (delta_y ** 2))), -1)
    indexes = np.where(dist_w_s<=10000)[0]

    if len(indexes) !=0:
        angle_w_s = np.round(((np.arctan2(delta_y[indexes], delta_x[indexes])) * 180 / np.pi) % 360, 1)
        index_angle= np.where(angle_w_s == possibleAngles)[0]
        indexes=indexes[index_angle]

        index_distance = (dist_w_s[indexes]/10).astype(int) # because bins every 10m
        probability = detection_probs[index_distance]

        detected_value = np.random.binomial(1, probability)
        indexes_detected_1=np.where(detected_value==1)[0].T
        indexes = indexes[indexes_detected_1]

        c=0
        for i in indexes:
            if int(whale_z[i]) == 0:  # at surface
                surface_whales_xyz = np.vstack((surface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                surface_ships_xy = np.vstack((surface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                if dist_w_s[i] > exclusion_distance:  # whale is in "in-time detectable_whales_xyz zone + at vulnerable_whales_xyz"
                    detection_whales_xyz = np.vstack(
                        (detection_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                    detection_ships_xy = np.vstack((detection_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                c=c+1
                break
            elif int(whale_z[i]) == 1:  # below surface
                subsurface_whales_xyz = np.vstack(
                    (subsurface_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
                subsurface_ships_xy = np.vstack((subsurface_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
                c=c+1
                break
    return detection_whales_xyz, detection_ships_xy, surface_whales_xyz, surface_ships_xy, subsurface_whales_xyz, subsurface_ships_xy



def detectability7(whale_x, whale_y, whale_z, ship_x, ship_y, possibleAngles, detectable_whales_xyz, detectable_ships_xy,
                   vulnerable_whales_xyz, vulnerable_ships_xy, exclusion_distance, detection_probs, detection_dist,
                   speed, ship_height, epoch, reaction_time,DDF,radius_detect):
    '''
   works! slightly faster than detectability5: distance = fist triage, then angle. USING MORE DICTIONARY
    '''

    import numpy as np

    #Compute whale/ship distance
    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    dist_w_s = np.round(np.sqrt(((delta_x ** 2) + (delta_y ** 2))), -1)
    indexes = np.where(dist_w_s <= 10000)[0]

    if len(indexes) != 0:
        # FILTER 1: DISTANCE WHALE/SHIP <10 000 m
        # Compute angle ship/whale
        angle_w_s = np.round(((np.arctan2(delta_y[indexes], delta_x[indexes])) * 180 / np.pi) % 360, 1)

        # FILTER 2: ANGLE WITHIN DETECTION RANGE
        # Find and save indexes where angles is valid (within possible detection  range)
        index_angle = np.where(angle_w_s == possibleAngles)[0]
        indexes = indexes[index_angle]

        if DDF == 1:  # data detection function (no harsh cut)


            # Start using curve data:
            # detection_distance= range of distances: 0-10000, step of 10
            # detection_probs= associated probabilities for each testing vessels

            index_distance = (dist_w_s[indexes] / 10).astype(int)  # can do that because bins every 10m
            probability = detection_probs[index_distance]

            detected_value = np.random.binomial(1, probability)  # gives out 1 or 0 values

            # FILTER 3:  KEEP ONLY INDEXES WHERE WHALE WAS DETECTED =1
            indexes_detected_1 = np.where(detected_value == 1)[0].T
            indexes = indexes[indexes_detected_1]

        else:  # harsh radius cut
            indexes = np.where(dist_w_s <= radius_detect)[0]

    name = 'epoch:' + str(epoch) + 'reaction_time:' + str(reaction_time) + 'ship_height:' + str(
        ship_height) + 'speed:' + str(
        speed)  # CAREFUL this name must match with main file for prob_detection storage

    for i in indexes:
        if int(whale_z[i]) == 0:  # detectable +< exclusion zone
            vulnerable_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
            vulnerable_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
            if dist_w_s[i] > exclusion_distance:  # detectable + > exclusion zone
                detectable_whales_xyz.setdefault(name, []).append(
                    [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
                detectable_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
            break
        elif int(whale_z[i]) == 1:  # vulnerable
            vulnerable_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
            vulnerable_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
            break
    return detectable_whales_xyz, detectable_ships_xy, vulnerable_whales_xyz, vulnerable_ships_xy




def detectability_lb(whale_x, whale_y, whale_z, ship_x, ship_y, possibleAngles, detected_whales_xyz, detected_ships_xy,
                     indanger_whales_xyz, indanger_ships_xy, exclusion_distance, detection_probs, detection_dist,
                     speed, ship_height, epoch, reaction_time, DDF, radius_detect):
    '''
   works! slightly faster than detectability5: distance = fist triage, then angle. USING MORE DICTIONARY
    '''

    import numpy as np

    #Compute whale/ship distance
    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    dist_w_s = np.round(np.sqrt(((delta_x ** 2) + (delta_y ** 2))), -1)
    indexes = np.where(dist_w_s <= 10000)[0]

    if len(indexes) != 0:
        # FILTER 1: DISTANCE WHALE/SHIP <10 000 m
        # Compute angle ship/whale
        angle_w_s = np.round(((np.arctan2(delta_y[indexes], delta_x[indexes])) * 180 / np.pi) % 360, 1)

        # FILTER 2: ANGLE WITHIN DETECTION RANGE
        # Find and save indexes where angles is valid (within possible detection  range)
        index_angle = np.where(angle_w_s == possibleAngles)[0]
        indexes = indexes[index_angle]

        if DDF == 1:  # data detection function (no harsh cut)
            # Start using curve data:
            # detection_distance= range of distances: 0-10000, step of 10
            # detection_probs= associated probabilities for each testing vessels

            index_distance = (dist_w_s[indexes] / 10).astype(int)  # can do that because bins every 10m
            probability = detection_probs[index_distance]
            detected_value = np.random.binomial(1, probability)  # gives out 1 or 0 values

            # FILTER 3:  KEEP ONLY INDEXES WHERE WHALE WAS DETECTED =1
            indexes_detected_1 = np.where(detected_value == 1)[0].T
            indexes = indexes[indexes_detected_1]

        else:  # harsh radius cut
            indexes_rad = np.where(dist_w_s[indexes] <= radius_detect)[0]
            indexes = indexes[indexes_rad]

        name = 'epoch:' + str(epoch) + 'reaction_time:' + str(reaction_time) + 'ship_height:' + str(
            ship_height) + 'speed:' + str(
            speed)  # CAREFUL this name must match with main file for prob_detection storage

        for i in indexes:
            if dist_w_s[i]>=exclusion_distance and whale_z[i]==0:
                detected_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
                detected_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
                break
            elif (dist_w_s[i]<exclusion_distance) and (whale_z[i]!=3):
                indanger_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
                indanger_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
               #break?

    # for i in indexes:
    #     if int(whale_z[i])!=3:  # any state but deep
    #         indanger_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
    #         indanger_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
    #         if dist_w_s[i] > exclusion_distance and int(whale_z[i]) == 0:  # whale in "in-time detection zone + blowing
    #             detected_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
    #             detected_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
    #         break


    return detected_whales_xyz, detected_ships_xy, indanger_whales_xyz, indanger_ships_xy



# def detect_DZ(whale_x,whale_y,whale_z,ship_x,ship_y,exclusion_distance,detection_probs):
#     import numpy as np
#
# #whale detection zone (blowing)/ whale_ exclusion zone (0,1,2)
#     delta_x = (whale_x - ship_x)
#     delta_y = (whale_y - ship_y)
#     dist_w_s = np.round(np.sqrt(((delta_x ** 2) + (delta_y ** 2))), -1)
#     #whales that ever entered exclusion zone
#     indexes=np.where(dist_w_s<=exclusion_distance)[0]
#     if len(indexes)==0:
#         break
#
#     index_distance = (dist_w_s[indexes] / 10).astype(int)  # can do that because bins every 10m
#     probability = detection_probs[index_distance]
#     detected_value = np.random.binomial(1, probability)
#     z_values=whale_z[indexes]
#     for i in range(len(indexes)):
#         if detected_value[i]==1 and z_values==


# if plot == 1:
    #     import matplotlib.pyplot as plt
    #     # for plotting sector lines
    #     # starting angle line
    #     startpt_x = np.cos(np.deg2rad(startAngle)) * radius_detect
    #     startpt_y = np.sin(np.deg2rad(startAngle)) * radius_detect
    #     # ending angle line
    #     endpt_x = np.cos(np.deindex_distance=int(np.where(detection_dist==dist_w_s)[0]) #get index of distance
    #     probability=detection_probs[index_distance] #associated probability for above distance
    #     detected_value = np.random.binomial(1, probability)
    #
    #     if detected_value==1:
    #         if int(whale_z[i]) == 0:  # at vulnerable_whales_xyz
    #             vulnerable_whales_xyz = np.vstack(
    #                 (vulnerable_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
    #             vulnerable_ships_xy = np.vstack((vulnerable_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
    #             if dist_w_s> exclusion_distance:  # whale is in "in-time detectable_whales_xyz zone + at vulnerable_whales_xyz"
    #                 detectable_whales_xyz = np.vstack(
    #                     (detectable_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
    #                 detectable_ships_xy = np.vstack((detectable_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
    #             break
    #         elif int(whale_z[i]) == 1:  # below vulnerable_whales_xyz
    #             vulnerable_whales_xyz = np.vstack(
    #                 (vulnerable_whales_xyz, [int(whale_x[i]), int(whale_y[i]), int(whale_z[i])]))
    #             vulnerable_ships_xy = np.vstack((vulnerable_ships_xy, [int(ship_x[i]), int(ship_y[i])]))
    #             break
    #     return detectable_whales_xyz, detectable_ships_xy, vulnerable_whales_xyz, vulnerable_ships_xy, vulnerable_whales_xyz, vulnerable_ships_xy

# if plot == 1:
    #     import matplotlib.pyplot as plt
    #     # for plotting sector lines
    #     # starting angle line
    #     startpt_x = np.cos(np.deg2rad(startAngle)) * radius_detect
    #     startpt_y = np.sin(np.deg2rad(startAngle)) * radius_detect
    #     # ending angle line
    #     endpt_x = np.cos(np.deg2rad(endAngle)) * radius_detect
    #     endpt_y = np.sin(np.deg2rad(endAngle)) * radius_detect
    #     plt.plot(xw, yw, 'y*', label='whale')  # plot whale position
    #     plt.plot(xs, ys, 'radius_detect*', label='ship')  # plot ship position
    #     plt.plot(startpt_x, startpt_y, 'c<', label='start Angle pt')  # start angle logo
    #     plt.plot(endpt_x, endpt_y, 'm>', label='End Angle pt')  # end angle logo
    #     plt.plot([0, startpt_x, 0, endpt_x], [0, startpt_y, 0, endpt_y], label='sector lines')  # plot sector lines
    #
    #     if np.size(detectable_whales_xyz, 0) != 1:
    #         plt.plot(detectable_whales_xyz[1:, 0], detectable_whales_xyz[1:, 1], "ro", label="In zone: Surface/Outside Exclusion zone (%d)"
    #                                                                  % (np.size(detectable_whales_xyz, 0) - 1))
    #     # ##At vulnerable_whales_xyz
    #     if np.size(vulnerable_whales_xyz, 0) != 1:
    #         plt.plot(vulnerable_whales_xyz[1:, 0], vulnerable_whales_xyz[1:, 1], "go", label="In zone: At vulnerable_whales_xyz (%d)" % (np.size(vulnerable_whales_xyz, 0) - 1))
    #
    #     ## Under vulnerable_whales_xyz
    #     if np.size(vulnerable_whales_xyz, 0) != 1:
    #         plt.plot(vulnerable_whales_xyz[1:, 0], vulnerable_whales_xyz[1:, 1], "yo",
    #                  label="In zone: Under vulnerable_whales_xyz (%d)" % (np.size(vulnerable_whales_xyz, 0) - 1))
    #
    #     plt.legend()
    # return detectable_whales_xyz, vulnerable_whales_xyz, vulnerable_whales_xyz, detected

# r=1000
# wx=200
# wy=300
# wz=0
# sx=0
# sy=0
# delta_x=0
# np.round(((np.arctan2(delta_y, delta_x)) * 180 / np.pi) % 360,1)
# detectability(1000, 200, 300,
#                     0, 0, 0,angle_w_s, dist_w_s, possibleAngles, detectable_whales_xyz,vulnerable_whales_xyz,
#                                                                      vulnerable_whales_xyz, speed, exclusion_distance, plot):

def detectability8(whale_x,whale_y,whale_z,ship_x,ship_y,possibleAngles,detection_whales_xyz, detection_ships_xy,
                      surface_whales_xyz, surface_ships_xy,
                      subsurface_whales_xyz, subsurface_ships_xy, exclusion_distance,detection_probs, detection_dist,speed,ship_height,epoch,reaction_time,radius_detect):
    '''
   works! slightly faster than detectability5: distance = fist triage, then angle. USING MORE DICTIONARY
   DOESN'T USE CURVES, ONLY RADIUS: HARD CUT AFTER RADIUS
    '''

    import numpy as np

    #Compute whale/ship distance
    delta_x = (whale_x - ship_x)
    delta_y = (whale_y - ship_y)
    dist_w_s = np.round(np.sqrt(((delta_x ** 2) + (delta_y ** 2))), -1)


    #FILTER 1: DISTANCE WHALE/SHIP <10 000 m
    indexes = np.where(dist_w_s<=radius_detect)[0]

    if len(indexes) !=0:

        #Compute angle ship/whale
        angle_w_s = np.round(((np.arctan2(delta_y[indexes], delta_x[indexes])) * 180 / np.pi) % 360, 1)

        #FILTER 2: ANGLE WITHIN DETECTION RANGE
        #Find and save indexes where angles is valid (within possible detection  range)
        index_angle= np.where(angle_w_s == possibleAngles)[0]
        indexes=indexes[index_angle]

        name = 'epoch:' + str(epoch) + 'reaction_time:' + str(reaction_time) + 'ship_height:' + str(ship_height) + 'speed:' + str(
            speed) #CAREFUL this name must match with main file for prob_detection storage

        for i in indexes:
            if int(whale_z[i]) == 0 or int(whale_z[i]) == 3:  # at surface
                surface_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
                surface_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])

                if dist_w_s[i] > exclusion_distance and int(whale_z[i]) == 3:  # whale in "in-time detection zone + at surface"
                    detection_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
                    detection_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
                break
            elif int(whale_z[i]) == 1:  # below surface
                subsurface_whales_xyz.setdefault(name, []).append([int(whale_x[i]), int(whale_y[i]), int(whale_z[i])])
                subsurface_ships_xy.setdefault(name, []).append([int(ship_x[i]), int(ship_y[i])])
                break
    return detection_whales_xyz, detection_ships_xy, surface_whales_xyz, surface_ships_xy, subsurface_whales_xyz, subsurface_ships_xy