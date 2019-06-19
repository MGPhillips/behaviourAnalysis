
import csv
import yaml
from os import walk
import h5py
import re
from nptdms import TdmsFile
import numpy as np
from pylab import *

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

                audio_completed = True

            if ind_type == 'Audio Stimulis':
                for obj in tdms_file.group_channels(ind_type):
                    string = obj.channel.split('-')[0]

                    indices.append(int(string.replace(" ", "")))

                audio_completed = True

        if not visual_completed and ind_type in visual_keys:

            if ind_type == 'Visual Stimulis':
                for obj in tdms_file.group_channels(ind_type):
                    string = obj.channel.split('-')[0]

                    indices.append(int(string.replace(" ", "")))

                visual_completed = True

            if ind_type == 'Visual Stimulation':
                indices = indices + [
                    x for x in np.where(tdms_file.group_channels(ind_type)[1].data != 0)[0]]

                visual_completed = True

    return indices

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

def get_mean_shelter_location(shelter_locations, nest_dict):

    for key in nest_dict:
        x_mean, y_mean = 0, 0
        for i, coord in enumerate(nest_dict[key]):
            if i == 0:
                continue
            x_mean += coord[0]
            y_mean += coord[1]

        x_mean, y_mean = x_mean / 5, y_mean / 5

        shelter_locations[key] = [x_mean, y_mean]

    return shelter_locations

#############with open('E:\\big_arena_analysis\\nest_locations.csv', 'w') as f:  # Just use 'w' mode in 3.x

    #w = csv.writer(f)
    #w.writerows(nest_dict.items())

#nest_dict

def build_data_dict(h5_directories, tdms_directories, exp_info, DLC_network, to_exclude):

    data_dict = {}

    for i, file in enumerate(h5_directories):

        print(file)
        slash_pos = [pos for pos, char in enumerate(file) if char == '\\']
        # print(slash_pos)

        exp_name_len = slash_pos[-1] - slash_pos[-2]

        exp_name = file[slash_pos[-1] + 1:slash_pos[-1] + exp_name_len + 1]

        try:
            experiment_info = exp_info[exp_name[:-1]]

            if experiment_info['mouse_id'] not in recent_mice:
                print('Mouse', experiment_info['mouse_id'], 'not in recent_mice')
                continue
        except:
            print('No exp info for', exp_name)

        if DLC_network in file:  # and file[49:59] not in to_exclude: #in shelter_locations:

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

                # fix_tracking(traj_x, traj_y, zeros_fun, 50)

                data_dict[exp_name]['x'], data_dict[exp_name]['y'] = traj_x, traj_y
                data_dict[exp_name]['head_x'], data_dict[exp_name]['head_y'] = head_x, head_y
                data_dict[exp_name]['tail_x'], data_dict[exp_name]['tail_y'] = tail_x, tail_y

                try:
                    # experiment_info = exp_info[exp_name[:-1]]

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
                        data_dict[exp_name]['stimulus_indices'] = get_tdms_indexes(tdms_dir)

    return data_dict

