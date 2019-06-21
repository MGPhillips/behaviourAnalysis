
import pandas as pd
from os import walk
import yaml

import sys
sys.path.insert(0, r'C:\Users\matthewp.W221N\Documents\GitHub\behaviourAnalysisMP\analysis')

from analysis_functions import *

from data_processing_functions import *
from load_functions import *
from loadsave_pickle import *
#from ./config/config.yml import
# TODO: Manage imports, setup exp info

load_data_df_from_pickle = True
save_out_data_df = False

load_flight_df_from_pickle = False
save_out_flight_df = True

produce_data_df = False

generate_flight_df = True

exp_info = {}
exp_info_path = 'E:\\big_arena_analysis\\dwm_darklight_analysis.csv'

exp_info = populate_exp_info(exp_info, exp_info_path)

if produce_data_df:

    dark_base = 'E:\\Dropbox (UCL - SWC)\\big_Arena\\experiments\\dwm\\data\\dark'
    light_base = 'E:\\Dropbox (UCL - SWC)\\big_Arena\\experiments\\dwm\\data\\basic'

    DLC_network = 'DeepCut_resnet50_Phillips_MG_700000'

    to_exclude = ['180402_longrange_nowall_2a', '180402_longrange_nowall_3a', '180422_dwm_240_2a',
                  '18MAY15_2404_DM', '18MAY15_2404_DM', '18MAY15_2403_DM']

    h5_directories, tdms_directories = get_directories(exp_info, to_exclude)

    data_dict = build_data_dict(h5_directories, tdms_directories, exp_info, DLC_network, to_exclude)

    data_df = pd.DataFrame.from_dict(data_dict, orient='index')

    save_pd_to_pickle(data_df, r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\data_df')


if load_data_df_from_pickle:

    data_df = load_pickle_to_pandas(r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\data_df')

if generate_flight_df:

    nest_dict = {}
    nest_dict = load_nest_info(nest_dict, 'E:\\big_arena_analysis\\nest_locations.csv')

    shelter_locations = {}
    shelter_locations = get_mean_shelter_location(shelter_locations, nest_dict)

    data_df = apply_proccessing_data_df(data_df, shelter_locations)
    flight_df = produce_flight_df(data_df, exp_info)

if save_out_flight_df:
    save_pd_to_pickle(flight_df, r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\flight_df')