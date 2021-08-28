def get_info_for_dp(mode):
    import pickle
    import os
    info=pickle.load(open(os.getcwd()+'/DATA/info_for_dp.pickle','rb'))
    if mode=='shallow':
        vec1=info['vec1_s']
        vec2=info['vec2_s']
        vec3=info['vec3_s']
        two_one=info['two_one_s']
        two_three=info['two_three_s']
    elif mode=='deep':
        vec1 = info['vec1_d']
        vec2 = info['vec2_d']
        vec3 = info['vec3_d']
        two_one = info['two_one_d']
        two_three = info['two_three_d']
    elif mode=='mixed':
        vec1 = info['vec1_m']
        vec2 = info['vec2_m']
        vec3 = info['vec3_m']
        two_one = info['two_one_m']
        two_three = info['two_three_m']
    return vec1,vec2,vec3,two_one,two_three
