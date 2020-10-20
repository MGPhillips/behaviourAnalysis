import pandas as pd
from os import walk
#import yaml

import sys

sys.path.insert(0, r'C:\Users\matthewp.W221N\Documents\GitHub\behaviourAnalysisMP\analysis')

from analysis_functions import *

from data_processing_functions import *
from load_functions import *
from loadsave_pickle import *
#from ./config/config.yml import
# TODO: Manage imports, setup exp info

load_data_df_from_pickle = False
save_out_data_df = True

load_flight_df_from_pickle = False
save_out_flight_df = True

produce_data_df = True

generate_flight_df = True
mouserotation = False


exp_info = {}

#exp_info_path = 'E:\\big_arena_analysis\\dwm_darklight_analysis.csv'
#exp_info_path = 'E:\\big_arena_analysis\\hc_lesion_analysis.csv'
#exp_info_path = 'E:\\big_arena_analysis\\mouse_rotation_analysis.csv'

#exp_info_path = 'E:\\big_arena_analysis\\dwm_trial_analysis.csv'

#exp_info_path = 'E:\\legacy\\big_arena_analysis\\dwm_darklight_analysis.csv'
exp_info_path = 'E:\\legacy\\big_arena_analysis\\shelter_raise_trial_analysis.csv'
exp_info = populate_exp_info(exp_info, exp_info_path)

if produce_data_df:

    dark_base = 'E:\\Dropbox (UCL - SWC)\\big_Arena\\experiments\\dwm\\data\\dark'
    light_base = 'E:\\Dropbox (UCL - SWC)\\big_Arena\\experiments\\dwm\\data\\basic'

    #DLC_networks = ['DeepCut_resnet50_Phillips_MG_700000', 'DeepCut_resnet50_BigArena2May8shuffle1_800000']

    DLC_networks = ['DLC_resnet50_lightdark_200226Feb26shuffle1_650000']#['cam1_FECDeepCut_resnet50_phillips_mg_800000']# ['DeepCut_resnet50_phillips_mg_700000']

    to_exclude = []#'180402_longrange_nowall_2a', '180402_longrange_nowall_3a', '180422_dwm_240_2a',
    #              '18MAY15_2404_DM', '18MAY15_2404_DM', '18MAY15_2403_DM', '190515_mouserotation_dark_630_1a',
    #              '190528_mouserotation_dark_677_1a', '190528_mouserotation_dark_677_1']

    h5_directories, tdms_directories = get_directories(exp_info, to_exclude)

    for x in h5_directories:
        if DLC_networks[0] not in x:
            print('NO DLC NETWORK IN:',x)

    h5_directories = [x for x in h5_directories if DLC_networks[0] in x]



    data_dict = build_data_dict(h5_directories, tdms_directories, exp_info, DLC_networks, to_exclude)

    data_df = pd.DataFrame.from_dict(data_dict, orient='index')

    #save_pd_to_pickle(data_df, r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\data_df_newnet_nondistflight') #r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\data_df_dwm'
    save_pd_to_pickle(data_df, r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\data_df_shelter_raise')

if load_data_df_from_pickle:

    data_df = load_pickle_to_pandas(r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\data_df')

if load_flight_df_from_pickle:

    flight_df = load_pickle_to_pandas(r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\flight_df')

    print('Flight dataframe loaded')

if generate_flight_df:

    #nest_dict = {}
    #nest_dict = load_nest_info(nest_dict, 'E:\\big_arena_analysis\\nest_locations.csv')

    #nest_df = load_nest_df_from_csv(r'C:\Users\matthewp.W221N\Desktop\nest_positions_mouse_rotation1.csv')  #nest_positions_mouse_rotation.csv #C:\Users\matthewp.W221N\Desktop\nest_positions2.csv

    #nest_df = load_nest_df_from_csv(r'C:\Users\matthewp.W221N\Desktop\nest_positions_hc.csv')

    #nest_df = load_nest_df_from_csv(r'C:\Users\matthewp.W221N\Desktop\nest_positions2.csv')#'C:\Users\matthewp.W221N\Desktop\nest_positions_dwm.csv') #r'C:\Users\matthewp.W221N\Desktop\nest_positions2.csv'
    nest_df = load_nest_df_from_csv(r'C:\Users\matthewp.W221N\Desktop\sraise_nest_position.csv')
    #print(nest_dict)
    #print(nest_df)

    shelter_locations = {}
    #print('Got to generate_flight_df')
    shelter_locations = get_mean_shelter_location(shelter_locations, nest_df)

    #print(shelter_locations)

    data_df = apply_proccessing_data_df(data_df, shelter_locations)
    flight_df = produce_flight_df(data_df, exp_info)

    print('Flight dataframe generated')

if save_out_flight_df:
    #save_pd_to_pickle(flight_df, r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\flight_df_dwm_newnet_nondistflight') #r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\flight_df_dwm'
    save_pd_to_pickle(flight_df, r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\flight_df_shelter_raise')
