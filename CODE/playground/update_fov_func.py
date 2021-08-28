
##Initialize
# gamma = beta_ship
# pmax = beta_ship + pan_angle / 2
# pmin = beta_ship - pan_angle / 2
# gamma_max = pmax - angle / 2
# gamma_min = pmin + angle / 2

def update_fov(rate, angle, beta_ship,gamma,gamma_max,gamma_min):
    import numpy as np
    import matplotlib.pyplot as plt

    # add radius_detect to inputs if wanting to plot
    # radius_detect = 300

    if gamma < gamma_min or gamma > gamma_max:
        rate = (-1) * rate

    gamma = gamma + rate
    gamma_ship = (gamma + beta_ship) % 360  # take modulus
    gamma_world = (gamma - 90) % 360
    gammas = (gamma, gamma_ship, gamma_world)

    startAngle = (gamma - angle / 2)
    endAngle = (gamma + angle / 2)%360
    angles = (startAngle, endAngle,gamma)

    # # # # PLOTTING
    # # for plotting ship trajectory
    # xs = np.linspace(0, 100)
    # x = np.cos(np.deg2rad(beta_ship)) * xs
    # y = np.sin(np.deg2rad(beta_ship)) * xs
    #
    # # gamma lines
    # gamma_x= np.cos(np.deg2rad(gamma)) * radius_detect
    # gamma_y = np.sin(np.deg2rad(gamma)) * radius_detect
    #
    # # for plotting max pan lines
    # pmax_x = np.cos(np.deg2rad(pmax)) * radius_detect
    # pmax_y = np.sin(np.deg2rad(pmax)) * radius_detect
    # # ending angle line
    # pmin_x = np.cos(np.deg2rad(pmin)) * radius_detect
    # pmin_y = np.sin(np.deg2rad(pmin)) * radius_detect
    #
    # # for plotting sector lines
    # # starting angle line
    # startpt_x = np.cos(np.deg2rad(startAngle)) * radius_detect
    # startpt_y = np.sin(np.deg2rad(startAngle)) * radius_detect
    # # ending angle line
    # endpt_x = np.cos(np.deg2rad(endAngle)) * radius_detect
    # endpt_y = np.sin(np.deg2rad(endAngle)) * radius_detect
    #
    # # Plotting vulnerable_whales_xyz parameters
    # # plt.plot(xw, yw, 'y*')  # plot whale position
    # plt.plot(0, 0, 'ro',label='ship')  # plot ship position
    # plt.plot(x, y, "-radius_detect", label='ship trajectory, Heading= (%d)°' % beta_ship)  # plot ship trajectory
    # plt.plot([0,gamma_x],[0,gamma_y], label='gamma direction, Gamma= (%d)°' %gamma)
    # plt.plot([0, startpt_x, 0, endpt_x], [0, startpt_y, 0, endpt_y], label='sector lines, Detection angle= '
    #                                                                        '(%d)°' % angle) # plot sector lines
    # plt.plot([0, pmax_x, 0, pmin_x], [0, pmax_y, 0, pmin_y], label='pan lines, Pan Angle= (%d)°' %pan_angle)
    #                                                                             # plot pan lines
    # plt.legend(loc=0)
    # plt.title('Update FOV function')
    # #plt.tight_layout()
    # plt.show()

    return angles
