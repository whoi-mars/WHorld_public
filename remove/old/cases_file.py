#   Creates JSON file
def cases_files_creation(new_folder):
    import json
    import csv
    cases_overall = {

        # #SANITY CHECKS

        "case1":
        # ALL BLOW,VW=0,RDR
            {
                "epoch number": 1,
                "run time (s)": 500,
                "grid width (m)": 4000,
                "ship height (m)": [1500, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1],#, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 100,
                "mean whale velocity (m/s)": 0,
                "std whale velocity (m/s)": 0,
                "Interval btw blows (s)": 60,
                "All whales blow": True,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": [],
            },

        "case2":
        # ALL SURFACE,VW=0,RDR
            {
                "epoch number": 10,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [1500, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 100,
                "mean whale velocity (m/s)": 0,
                "std whale velocity (m/s)": 0,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": True,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": [],
            },

        "case3":
        # ALL SUBSURFACE,VW=0,RDR
            {
                "epoch number": 10,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [1500, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 100,
                "mean whale velocity (m/s)": 0,
                "std whale velocity (m/s)": 0,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": True,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": [],
            },

        "case4":
        # ALL DEEP,VW=0,RDR
            {
                "epoch number": 10,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [1500, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 100,
                "mean whale velocity (m/s)": 0,
                "std whale velocity (m/s)": 0,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": True,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": [],
            },
        #####WHALE SPEEDS###
        "case5":
        # WHALE SPEED:0, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500,1000,1500,2000,3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 0,
                "std whale velocity (m/s)": 0,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        "case6":
        # WHALE SPEED:1, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 1,  # print ETA at after each run
                "Keep?": [],
            },

        "case7":
        # WHALE SPEED:2, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 2,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        "case8":
        # WHALE SPEED:3, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 3,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        #####interval blow###
        "case9":
        # INTERVAL BLOW=15, RDR
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 15,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
        #
        "case10":
        # INTERVAL BLOW=30, RDR
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 30,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        "case11":
        # INTERVAL BLOW=60, RDR
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        "case12":
        # INTERVAL BLOW=120, RDR
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 0,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 120,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        ####DDF####
        # case 13a: INTERVAL BLOW=15, DDF: see case 9

        # INTERVAL BLOW 15, DDF
        "case13":
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 15,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        "case14":
        # INTERVAL BLOW=30, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 30,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        # INTERVAL BLOW 60, DDF
        "case15":
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        "case16":
        # INTERVAL BLOW=120, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 120,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'mixed',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
        # SHALLOW IBI:
        "case17":
        # INTERVAL BLOW=15, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 15,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'shallow',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
        "case18":
        # INTERVAL BLOW=30, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 30,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'shallow',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
        "case19":
        # INTERVAL BLOW=60, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'shallow',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
        "case20":
        # INTERVAL BLOW=120, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 120,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'shallow',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        # DEEP IBI:
        "case21":
        # INTERVAL BLOW=15, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 15,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'deep',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
        "case22":
        # INTERVAL BLOW=30, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 30,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'deep',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },

        "case23":
        # INTERVAL BLOW=60, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 60,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'deep',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
        "case24":
        # INTERVAL BLOW=120, DDF
            {
                "epoch number": 1,
                "run time (s)": 3600,
                "grid width (m)": 4000,
                "ship height (m)": [500, 1000, 1500, 2000, 3000],  # really DDF value now
                "ship number": 3,
                "ship speeds (m/s)": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "ship heading (deg)": 90,
                "angle of detection (deg)": 20,
                "data detection function": 1,  # 1=no harsh radius cut for detection
                "ship reaction time (s)": [60, 120],
                "whale number": 1000,
                "mean whale velocity (m/s)": 1,
                "std whale velocity (m/s)": 0.2,
                "Interval btw blows (s)": 120,
                "All whales blow": False,  # only 1 option below can be true, if none= true dp
                "All whales surface": False,
                "All whales subsurface": False,
                "All whales deep": False,
                "dive profile mode": 'deep',
                # if one of the 3 above is true, no random dive profile
                "plot probabilities": True,
                "plot world": True,
                "ETA display": 0,  # print ETA at after each run
                "Keep?": 'K',
            },
    }

    # CREATE JSON FILES
    i = 1
    for cases in cases_overall:
        case_name = 'case' + str(i)
        j = json.dumps(cases_overall[case_name])

        with open("./CASES_RUN/" + case_name, 'w') as f:
            f.write(j)
            f.close()
            print('JSON # (%d) FILE CREATED!' % i)
        i = i + 1

    # SAVE INTO CSV FILE
#WORKS
    destination="./RUN_RESULTS/"+str(new_folder)+"/cases_file.csv"
    with open(destination, 'w') as f:
        # Using dictionary keys as fieldnames for the CSV file header
        writer = csv.DictWriter(f, cases_overall['case1'].keys())
        writer.writeheader()
        for d in cases_overall:
            writer.writerow(cases_overall[d])
