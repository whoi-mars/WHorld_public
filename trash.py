from CODE.functions import f_dive_profile

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

