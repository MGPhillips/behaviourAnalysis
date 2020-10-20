
import csv
#import yaml
import pandas as pd
from os import walk
import h5py
import re
from nptdms import TdmsFile
import numpy as np
from itertools import chain
from pylab import *

from load_functions import *
from data_processing_functions import *

def load_yaml(fpath):
    """ load settings from a yaml file and return them as a dictionary """
    with open(fpath, 'r') as f:
        settings = yaml.load(f)
    return settings

def load_paths():
    """ load PATHS.yml to set all the user-specific paths correctly """
    filename = './PATHS.yml'
    return load_yaml(filename)

def get_directories(exp_info, to_exclude):
    bases = []
    h5_directories = []
    tdms_directories = []

    for key in exp_info:
        bases.append(exp_info[key]['base_folder'] + '\\' + key)

    for base in bases:
        for exc in to_exclude:
            if exc in base:
                continue

        h5_direct, filenames = get_filetype_paths('.h5', base)

        tdms_direct, filenames = get_filetype_paths('.tdms', base)
        h5_directories = h5_directories + h5_direct
        tdms_directories = tdms_directories + tdms_direct

    return h5_directories, tdms_directories

def get_filetype_paths(filetype, base):
    # Takes a desired filetype and a base directory and returns a list of their locations
    # within it's subdirectories

    # Set up file location list
    fpath = []
    f = []

    # Search through folders
    for (dirpath, dirnames, filenames) in walk(base):

        # if a file is detected, enter detection of its type append to list
        if filenames:
            for file in filenames:

                # If filetype matches the desired, append to list
                if file.endswith(filetype):
                    fpath.append(dirpath + '/' + file)  #
                    f.append('/' + file)

    return fpath, f

def get_tdms_indexes(path):

    indices = []
    stim_types = []
    tdms_file = TdmsFile(path)

    audio_completed = False
    visual_completed = False
    audio_keys = ['Audio Stimulation', 'Audio Stimulis']
    visual_keys = ['Visual Stimulation', 'Visual Stimulis']

    for ind_type in tdms_file.groups():

        if not audio_completed and ind_type in audio_keys:

            if ind_type == 'Audio Stimulation':
                indices = indices + [
                    x for x in np.where(tdms_file.group_channels(ind_type)[1].data != 0)[0]]
                stim_types.append('Audio')
                audio_completed = True

            if ind_type == 'Audio Stimulis':
                for obj in tdms_file.group_channels(ind_type):
                    string = obj.channel.split('-')[0]

                    indices.append(int(string.replace(" ", "")))

                stim_types.append('Audio')
                audio_completed = True

        if not visual_completed and ind_type in visual_keys:

            if ind_type == 'Visual Stimulis':
                for obj in tdms_file.group_channels(ind_type):
                    string = obj.channel.split('-')[0]

                    indices.append(int(string.replace(" ", "")))
                stim_types.append('Visual')
                visual_completed = True

            if ind_type == 'Visual Stimulation':
                indices = indices + [
                    x for x in np.where(tdms_file.group_channels(ind_type)[1].data != 0)[0]]
                stim_types.append('Visual')
                visual_completed = True

    return indices, stim_types

def populate_exp_info(exp_info, csv_path):

    reader = csv.DictReader(open(csv_path))

    for row in reader:
        key = row['experiment']
        if key in exp_info:
            pass

        exp_info[key] = {}

        for ind in row:
            if ind == 'experiment':
                continue
            exp_info[key][ind] = row[ind]

    return exp_info

def group(lst, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]

    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.

    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)])

def load_nest_info(nest_dict, nest_info_path):
    #'E:\\big_arena_analysis\\nest_locations.csv'
    with open(nest_info_path, 'r') as f:
        read = csv.reader(f, delimiter=',')
        for row in read:
            if len(row) == 0:
                continue

            nest_dict[row[0]] = [list(x) for x in list(group([int(x) for x in re.findall(r"[\w']+", row[1])], 2))]

    return nest_dict

def get_mean_shelter_location(shelter_locations, nest_df):

    for key in nest_df:
        x_mean, y_mean = 0, 0
        print('Key:', key, 'Nest df:', nest_df[key])
        for i, coord in enumerate(nest_df[key]):
            if i == 0:
               continue

            print()

            coords = [int(x) for x in nest_df[key][i].replace('[','').replace(']','').replace(' ','').split(',')]

            x_mean += coords[0]
            y_mean += coords[1]

        x_mean, y_mean = x_mean / 4, y_mean / 4

        shelter_locations[key] = [x_mean, y_mean]

    return shelter_locations

def save_out_nest_positions(path, nest_dict):

    with open(path, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(nest_dict.keys())
        writer.writerows(zip(*nest_dict.values()))

def load_nest_df_from_csv(path):

    return pd.read_csv(path)

#############with open('E:\\big_arena_analysis\\nest_locations.csv', 'w') as f:  # Just use 'w' mode in 3.x

    #w = csv.writer(f)
    #w.writerows(nest_dict.items())

#nest_dict

def build_data_dict(h5_directories, tdms_directories, exp_info, DLC_networks, to_exclude):

    data_dict = {}

    #recent_mice = ['413_1', '413_2', '413_3', '413_4', '445_1', '447_2', '447_3', '447_4', '551_1', '620_1', '620_3', '445_5', '445_3', '445_2', '445_4',
    #               '550_1', '551_5', '551_2', '551_3', '551_4', '551_5', '619_1', '619_2', '619_3', '620_2', '708_1', '707_1', '706_1', '705_1', '704_1',
    #               '672_1', '674_4', '671_1', '668_1', '670_1', '669_1', '677_1', '674_1', '672_1', '668_1', '672_1', '654_1', '669_1', '676_1', '675_1',
    #               '673_1', '668_1', '654_1', '623_1', '622_1', '621_1', '630_1', '625_1', '319_3', '319_4', '319_5', '320_4', '320_3', '337_2', '337_1'
    #               '370_3', '370_4', '370_1', ]

    for i, file in enumerate(h5_directories):

        print(file)
        slash_pos = [pos for pos, char in enumerate(file) if char == '\\']
        # print(slash_pos)

        exp_name_len = slash_pos[-1] - slash_pos[-2]

        exp_name = file[slash_pos[-1] + 1:slash_pos[-1] + exp_name_len + 1]

        print(exp_name)

        try:
            experiment_info = exp_info[exp_name[:-1]]
            print(exp_info[exp_name[:-1]])
            #if experiment_info['mouse_id'] not in recent_mice:
            #    print('Mouse', experiment_info['mouse_id'], 'not in recent_mice')
            #    continue
        except:
            print('No exp info for', exp_name)

        if any(dlc in file for dlc in DLC_networks):  # and file[49:59] not in to_exclude: #in shelter_locations:

            print('Loading...', exp_name)

            with h5py.File(file, 'r') as f:

                if exp_name in to_exclude:
                    continue

                data_dict[exp_name] = {}

                traj_x, traj_y, head_x, head_y, tail_x, tail_y = [], [], [], [], [], []

                for j, data in f['df_with_missing']['table']:
                    traj_x.append(data[3])
                    traj_y.append(data[4])

                    head_x.append(data[0])
                    head_y.append(data[1])

                    tail_x.append(data[6])
                    tail_y.append(data[7])

                traj_x, traj_y = np.asarray(traj_x), np.asarray(traj_y)
                head_x, head_y = np.asarray(head_x), np.asarray(head_y)
                tail_x, tail_y = np.asarray(tail_x), np.asarray(tail_y)

                fix_tracking(traj_x, traj_y, zeros_fun, 50)

                data_dict[exp_name]['x'], data_dict[exp_name]['y'] = traj_x, traj_y
                data_dict[exp_name]['head_x'], data_dict[exp_name]['head_y'] = head_x, head_y
                data_dict[exp_name]['tail_x'], data_dict[exp_name]['tail_y'] = tail_x, tail_y

                try:
                    experiment_info = exp_info[exp_name[:-1]]

                    data_dict[exp_name]['experiment_type'] = experiment_info['expt_type']
                    data_dict[exp_name]['mouse_id'] = experiment_info['mouse_id']

                except:
                    print(file, '... no exp info for file')

                if exp_name[-1] == experiment_info['dwm_trial']:
                    data_dict[exp_name]['dwm_trial'] = True

                elif exp_name[-1] != experiment_info['dwm_trial']:
                    data_dict[exp_name]['dwm_trial'] = False

                for tdms_dir in tdms_directories:
                    if exp_name in tdms_dir:
                        data_dict[exp_name]['stimulus_indices'], data_dict[exp_name]['stimulus_types'] = get_tdms_indexes(tdms_dir)

    return data_dict

