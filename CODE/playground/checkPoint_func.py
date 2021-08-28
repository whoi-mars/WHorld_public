def checkPoint(r, xp, yp, zp, xc, yc, startAngle,endAngle, detection, present, submerged):
    """
         :param xs,ys: ship positions
         :param xw,yw,zw: whale positions
         startAngle: from FOV function
         endEngle: from FOV function
         """

    import numpy as np
    import math

    A = xp - xc
    B = yp - yc
    maxlength = round(np.sqrt(((A ** 2) + (B ** 2))))
    angle_w_s = round(math.degrees(math.acos(A / math.sqrt((A ** 2) + (B ** 2)))))

    if endAngle >= 360:
        endAngle = endAngle - 360

    # negative quadrants
    if startAngle > 180 and endAngle > 180:
        angle_w_s = 360 - angle_w_s

    # positive/negative case
    if startAngle <= 0 and endAngle >= 0:
        if B < 0:
            angle_w_s = -angle_w_s

    # between 180+/0+ case
    if (startAngle >= 180 and endAngle >= 0 and maxlength <= r):
        if B < 0:
            angle_w_s = 360 - angle_w_s

        pA = np.arange(startAngle, 361, 1)
        pB = np.arange(0, endAngle + 1, 1)
        possible_angles = np.append(pA, pB)

        if angle_w_s in possible_angles:
            if int(zp) == 0:  # at vulnerable_whales_xyz
                detection = np.vstack((detection, [xp, yp, zp]))
            elif int(zp) == 1:  # below vulnerable_whales_xyz
                present = np.vstack((present, [xp, yp, zp]))
            else:  # ==2 well below vulnerable_whales_xyz
                submerged = np.vstack((submerged, [xp, yp, zp]))

    # check if angle_detection of whale is btw start/end angles and within radius of sector
    elif (angle_w_s >= startAngle and angle_w_s <= endAngle and maxlength <= r):
        if int(zp) == 0:  # at vulnerable_whales_xyz
            detection = np.vstack((detection, [xp, yp, zp]))
        elif int(zp) == 1:  # below vulnerable_whales_xyz
            present = np.vstack((present, [xp, yp, zp]))
        else:  # ==2 well below vulnerable_whales_xyz
            submerged = np.vstack((submerged, [xp, yp, zp]))

    results = (detection, present, submerged)
    return results

