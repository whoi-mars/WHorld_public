
def whorld_plt(ship_nb,ship_x,ship_y,beta_ship,angle_detection,time_run,startAngle,endAngle,radius_detect,whale_nb,
               whale_x,whale_y,ship_reaction_time,width,l,epoch,ship_height,indanger_whales_xyz,detected_whales_xyz,run_name,ship_speeds,output_destination):
    import matplotlib.pyplot as plt
    import numpy as np

    fig1 = plt.figure(figsize=(8, 8))
    fig1.tight_layout

    ##PLOTTING
    # font = {'family': 'normal',
    #         'weight': 'normal',
    #         'size': 13}
    # matplotlib.rc('font', **font)

    # SHIPS: last epoch/runtime/ship height,ship_speed
    for c in range(ship_nb):
        # Plotting ship POSITIONS
        plt.plot(ship_x[c], ship_y[c], 'v', label="Boat (%d)" % ship_nb if c == 0 else "")

        # Plotting ship (red) TRAJECTORY: works!
        x1 = ship_x[c][0]
        y1 = ship_y[c][0]
        o = 900
        if beta_ship > 90:
            ang = 90 - (beta_ship % 90)
            x2 = x1 - (o)
        else:
            ang = beta_ship
            x2 = x1 + (o)
        y2 = y1 + (o) * np.tan(np.deg2rad(ang))
        plt.plot([x1, x2], [y1, y2], '--r',
                 label='Ship Trajectory, Heading= (%d)°' % beta_ship if c == 0 else "")

        # Plotting SECTOR LINES
        if angle_detection != 360:
            for i in np.arange(0, time_run, 200):
                # starting angle_detection line
                startpt_x = np.cos(np.deg2rad(startAngle)) * radius_detect + ship_x[c][i]
                startpt_y = np.sin(np.deg2rad(startAngle)) * radius_detect + ship_y[c][i]
                # ending angle_detection line
                endpt_x = np.cos(np.deg2rad(endAngle)) * radius_detect + ship_x[c][i]
                endpt_y = np.sin(np.deg2rad(endAngle)) * radius_detect + ship_y[c][i]
                plt.plot([ship_x[c][i], startpt_x, ship_x[c][i], endpt_x],
                         [ship_y[c][i], startpt_y, ship_y[c][i], endpt_y], "-m",
                         label='Sector Lines, Angle of Detection= (%d)°' % angle_detection if i == 0 and c == 0 else "")
        else:  # Circles of detectable_whales_xyz, when angle_detection=360
            theta = np.linspace(0, 2 * np.pi, 100)  # for circle of detectable_whales_xyz
            for i in range(time_run):
                x1 = radius_detect * np.cos(theta) + ship_x[c][i]
                x2 = radius_detect * np.sin(theta) + ship_y[c][i]
                plt.plot(x1, x2)
                i = i + 100

    # WHALES:
    for d in range(whale_nb):
        plt.plot(whale_x[d], whale_y[d], "b.", label="Whale (%d)" % whale_nb if d == 0 else "")

    # DETECTION: on  last epoch/runtime/ship height,ship_speed
    # For plotting purposes, only look at last run
    last_rd_name = 'epoch:' + str(epoch - 1) + 'reaction_time:' + str(
        ship_reaction_time[-1]) + 'ship_height:' + str(ship_height[-1]) + 'speed:' + str(ship_speeds[-1])

    # In Danger
    if last_rd_name in indanger_whales_xyz:
        danger_whale_xyz = np.array(indanger_whales_xyz[last_rd_name])
        danger_whale_x = danger_whale_xyz[:, 0]
        danger_whale_y = danger_whale_xyz[:, 1]
        plt.plot(danger_whale_x, danger_whale_y, "go",
                 label="In Danger Whales (%d)" % len(danger_whale_xyz))
    # Detected
    if last_rd_name in detected_whales_xyz:
        det_whale_xyz = np.array(detected_whales_xyz[last_rd_name])
        det_whale_x = det_whale_xyz[:, 0]
        det_whale_y = det_whale_xyz[:, 1]
        plt.plot(det_whale_x, det_whale_y, "ro", label="Detectable (>Exclusion Zone) (%d)"
                                                       % len(det_whale_xyz))

    plt.axis([0, width, 0, l])
    plt.gca().set_aspect('auto')  # , adjustable='box')
    plt.xlabel('X Coordinates [m]')
    plt.ylabel('Y Coordinates [m]')
    plt.suptitle(run_name)
    plt.title('Ship Strike Mitigation Model, ship speed=%.2f m/s' % ship_speeds[-1])
    plt.gca().legend(title='Legend', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.grid()
    #plt.show()
    fig1.savefig(output_destination+'/'+ run_name + '_world' + '.png', bbox_inches='tight')


def probability_plt(ship_height,ship_speeds,prob_average_final,prob_std_final,ship_reaction_time,run_name,epoch,output_destination):
    import matplotlib.pyplot as plt

    fig2, axs2 = plt.subplots(1, len(ship_reaction_time), figsize=(15, 10))

    i = 0
    for r_time in ship_reaction_time:
        for ship_h in ship_height:
            #axs2[i].plot(ship_speeds, prob_average_final['reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h)],
                   #      label=str(ship_h) + 'm')
            axs2[i].errorbar(ship_speeds, prob_average_final['reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h)],
                             yerr=prob_std_final['reaction_time:' + str(r_time) + 'ship_height:' + str(ship_h)],
                             label=str(ship_h)+'m')
            axs2[i].legend()

        axs2[i].set_title('Reaction time: %d sec'%r_time)
        axs2[i].set_xlabel('Speed (m/s)')
        axs2[i].grid()
        axs2[i].set_ylim(-0.01, 1.01)

        i = i + 1
    fig2.suptitle(run_name + '\n \n' + 'In-time Detection Probability, #epoch=%i' % (epoch))
    fig2.tight_layout
    #plt.show()
    fig2.savefig(output_destination+'/'+ run_name + '_probs' + '.png', bbox_inches='tight')