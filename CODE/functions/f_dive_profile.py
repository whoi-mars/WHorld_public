'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SCRIPT CONTAINS ALL THE FUNCTIONS ASSOCIATED WITH THE CREATION OF ARTIFICIAL DIVE PROFILES

'''


def create_dive_profile(vec_1,vec_2,vec_3,two_one,two_three,interval_blow):
    #Step 2 for dp creation
    import numpy as np
    import random
    import pickle

    # Create artificial dive profile using length from real state vectors
    # 0: blow
    # 1: surface
    # 2: subsurface
    # 3: deep

    dive_profile = np.array([])
    l = random.choice([1, 2, 3])  # Random start state
    flag=0
    for i in range(300):  # change here if need longer dp
        if l == 1:  # surface
            A = int(random.choice(vec_1))
            vector1 = np.full((1, A), 1)
            # ADDING BLOWS: State 0
            if interval_blow != 0:
                k = 0
                for i in range(0, A):
                    vector1[0, k] = 0
                    vector1[0, k + 1] = 0
                    vector1[0, k + 2] = 0
                    k = k + 3 + interval_blow
                    if k > A - 3:
                        break
            dive_profile = np.append(dive_profile, vector1)
            flag=0
            l = 2
        elif l == 2:  # subsurface
            B = int(random.choice(vec_2))
            vector2 = np.full((1, B), 2)
            dive_profile = np.append(dive_profile, vector2)

            p=two_one/(two_one+two_three)

            #IF COME FROM DEEP STATE: MUST GO TO SURFACE
            if flag==1:
                p=1
            decision = np.random.binomial(1, p)
            if decision==1: #going from 2 to 1
                l=1
            else:
                l=3

        elif l == 3:  # deep
            C = int(random.choice(vec_3))
            vector3 = np.full((1, C), 3)
            dive_profile = np.append(dive_profile, vector3)
            l = 2
            flag=1
    return dive_profile



