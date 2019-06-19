

import pandas as pd
from os import walk
import yaml

from data_processing_functions import *
from load_functions import *
from loadsave_pickle import *
#from ./config/config.yml import
# TODO: Manage imports, setup exp info

#load_yaml

dark_base = 'E:\\Dropbox (UCL - SWC)\\big_Arena\\experiments\\dwm\\data\\dark'
light_base = 'E:\\Dropbox (UCL - SWC)\\big_Arena\\experiments\\dwm\\data\\basic'

DLC_network = 'DeepCut_resnet50_Phillips_MG_700000'

to_exclude = ['180402_longrange_nowall_2a', '180402_longrange_nowall_3a', '180422_dwm_240_2a',
              '18MAY15_2404_DM', '18MAY15_2404_DM', '18MAY15_2403_DM']

exp_info = {}
exp_info_path = 'E:\\big_arena_analysis\\dwm_darklight_analysis.csv'

exp_info = populate_exp_info(exp_info, exp_info_path)

h5_directories, tdms_directories = get_directories(exp_info, to_exclude)

data_dict = build_data_dict(h5_directories, tdms_directories, exp_info, DLC_network, to_exclude)

data_df = pd.DataFrame.from_dict(data_dict, orient='index')

save_pd_to_pickle(data_df, r'E:\Dropbox (UCL - SWC)\big_Arena\analysis\data_df')