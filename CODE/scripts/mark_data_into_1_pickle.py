'''FROM MARK'S DATA,
- read ALL Netcdf files
- compiles all VEC1/2/3 + STATE TRANSITION NUMBERS 2==>1, 2==>3 info for shallow/deep/mixed dive profiles
- save above info into 1 pickle file
- ==> enables running MAIN.py function without having access to Mark's NARW dive profiles!'''


import os
import pickle
# hacky import fix - don't do this
import sys


os.chdir('/home/loicka/Desktop/ws_whorld/organized_whorld')
prefix='/home/loicka/Desktop/ws_whorld/organized_whorld'  #todo modify here
output_destination='/home/loicka/Desktop/ws_whorld/organized_whorld/DATA'
def info_for_dp_funct(mode):
    #Step 1 for dp creation
    from CODE.functions import f_triage_repertoire_dp as tdp

    # LOAD/CREATE VEC1,2,3 FOR DP CONSIDERING CHOSEN MODE
    repertoire_dict = tdp.extract_good_segment('trimmed_repertoire_w_sdclass')  # yes
    rep = {}
    c = 0
    for i in range(len(repertoire_dict)):
        if mode == 'shallow':
            if repertoire_dict[i][1] == 's':
                rep[c] = repertoire_dict[i]
                c = c + 1
        elif mode == 'deep':
            if repertoire_dict[i][1] == 'd':
                rep[c] = repertoire_dict[i]
                c = c + 1
        elif mode == 'mixed':
            rep = repertoire_dict

    _, depth_state_dict = tdp.create_state_dps(rep)
    depth_state_array = tdp.transform_dict_into_array(depth_state_dict)
    two_one, two_three = tdp.count_transitions(depth_state_array)
    _, vec_1, vec_2, vec_3 = tdp.create_vect0123s(depth_state_dict)
    return vec_1,vec_2,vec_3,two_one,two_three

vec_1_s,vec_2_s,vec_3_s,two_one_s,two_three_s=info_for_dp_funct('shallow')
vec_1_d,vec_2_d,vec_3_d,two_one_d,two_three_d=info_for_dp_funct('deep')
vec_1_m,vec_2_m,vec_3_m,two_one_m,two_three_m=info_for_dp_funct('mixed')

content = {
    "vec1_s": vec_1_s,
    "vec2_s": vec_2_s,
    "vec3_s": vec_3_s,
    "two_one_s": two_one_s,
    "two_three_s": two_three_s,
    "vec1_d": vec_1_d,
    "vec2_d": vec_2_d,
    "vec3_d": vec_3_d,
    "two_one_d": two_one_d,
    "two_three_d": two_three_d,
    "vec1_m": vec_1_m,
    "vec2_m": vec_2_m,
    "vec3_m": vec_3_m,
    "two_one_m": two_one_m,
    "two_three_m": two_three_m,
}
pickle.dump(content, open(output_destination + '/' + 'info_for_dp' + '.pickle', "wb"))

