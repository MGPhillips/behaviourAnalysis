
import numpy as np
from pylab import *
import pandas as pd

def get_speed(row):

    traj_x, traj_y = row['x'], row['y']
    dx, dy = (traj_x[1:] - traj_x[:-1], traj_y[1:] - traj_y[:-1])
    distance_travelled = np.sqrt(d x* * 2 +d y* *2)

    return distance_travelled

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_vectors(row):
    vec_x, vec_y = np.ediff1d(row['x'], to_begin=0), np.ediff1d(row['y'], to_begin=0)
    vectors = np.array(list(zip(vec_x, vec_y)))
    return vectors

def get_head_tail_vectors(row):
    print(row.name)
    body_to_head_vector  = list(zip(np.subtract(row['head_x'], row['x']), np.subtract(row['head_y'], row['y'])))
    body_to_tail_vector = list(zip(np.subtract(row['tail_x'], row['x']), np.subtract(row['tail_y'], row['y'])))

    # print(body_to_head_vector)
    return body_to_head_vector, body_to_tail_vector

def compute_distance(coord1, coord2):

    dx, dy = (coord2[0] - coord1[0], coord2[1] - coord1[1])

    distance = np.sqrt(d x* * 2 +d y* *2)

    return distance

def flip_head_tail(row, i):

    head_x ,head_y ,tail_x ,tail_y = row['tail_x'][i], row['tail_y'][i], row['head_x'], row['head_y']

    return head_x, head_y, tail_x, tail_y



def correct_orientation(row):
    print(row.name)

    tail_x, tail_y, head_x, head_y = row['tail_x'], row['tail_y'], row['head_x'], row['head_y']

    # head_angle = [abs(180.- math.degrees(angle_between(row['vectors'][i], row['body_to_head_vector'][i])))
    #                  for i in range(len(row['body_to_head_vector']))]
    # tail_angle = [abs(180.- math.degrees(angle_between(row['vectors'][i], row['body_to_tail_vector'][i])))
    #              for i in range(len(row['body_to_tail_vector']))]

    # to_flip = np.where(np.array(tail_angle) < np.array(head_angle))[0]

    # for flip in to_flip:
    # print('Corrected...', row.name, flip)
    #   head_x[flip], head_y[flip], tail_x[flip], tail_y[flip] = tail_x[flip], tail_y[flip], head_x[flip], head_y[flip]

    # print('Length of to_flip:', len(to_flip))
    # print('to_flip:', to_flip)

    head_x_list, head_y_list, tail_x_list, tail_y_list = [], [], [], []
    count_a, count_d, count_f = 0, 0, 0
    to_flip = False

    for i, data in enumerate(row['head_x']):

        head_x_i, head_y_i, tail_x_i, tail_y_i = row['head_x'][i], row['head_y'][i], row['tail_x'][i], row['tail_y'][i]

        if to_flip:
            head_x_i, head_y_i, tail_x_i, tail_y_i =  tail_x_i, tail_y_i, head_x_i, head_y_i

        to_flip = False

        if i+ 2 < len(row['head_x']):

            head_x_i2, head_y_i2, tail_x_i2, tail_y_i2 = (
                row['head_x'][i + 1], row['head_y'][i + 1], row['tail_x'][i + 1], row['tail_y'][i + 1])

            mouse_vector = [head_x_i - tail_x_i, head_y_i - tail_y_i]
            mouse2_vector = [head_x_i2 - tail_x_i2, head_y_i2 - tail_y_i2]
            mouse2_vector_flip = [tail_x_i2 - head_x_i2, tail_y_i2 - head_y_i2]

            angle = angle_between(mouse_vector, mouse2_vector)
            flip_angle = angle_between(mouse_vector, mouse2_vector_flip)

            if angle > flip_angle:
                if count_a == 0:
                    print('Flipping first coords based on angle')

                to_flip = True
                count_a += 1

        #             head_to_next_head_distance = compute_distance([head_x_i, row['head_y'][i]],
        #                                                           [row['head_x'][i+1], row['head_y'][i+1]])

        #             tail_to_next_tail_distance = compute_distance([row['tail_x'][i], row['tail_y'][i]],
        #                                                           [row['tail_x'][i+1], row['tail_y'][i+1]])

        #             head_to_next_tail_distance = compute_distance([row['head_x'][i], row['head_y'][i]],
        #                                                           [row['tail_x'][i+1], row['tail_y'][i+1]])

        #             tail_to_next_head_distance = compute_distance([row['head_x'][i], row['head_y'][i]],
        #                                                           [row['head_x'][i+1], row['head_y'][i+1]])

        #             if (head_to_next_tail_distance ** 2 + tail_to_next_head_distance ** 2) < (
        #                 head_to_next_head_distance ** 2 + tail_to_next_tail_distance ** 2):
        #                     if count_d == 0:

        #                         print('Flipping first coords based on distance')
        #                     to_flip = True
        #                     count_d+=1

        #         if angle > flip_angle and (head_to_next_tail_distance ** 2 + tail_to_next_head_distance ** 2) > (
        #             head_to_next_head_distance ** 2 + tail_to_next_tail_distance ** 2):
        #             if count_f == 0:
        #                     print('Setting to false')
        #                     count_f+=1
        #             to_flip=False

        head_x_list.append(head_x_i), head_y_list.append(head_y_i)
        tail_x_list.append(tail_x_i), tail_y_list.append(tail_y_i)
    # head_x, head_y, tail_x, tail_y = row['tail_x'], row['tail_y'], row['head_x'], row['head_y']

    # head_x_i_prev, head_y_i_prev, tail_x_i_prev, tail_y_i_prev = head_x_i, head_y_i, tail_x_i, tail_y_i
    #   distance1 = compute_distance()
    #   distance2
    # print(head_x_list)
    print(count_a, count_d)
    return head_x_list, head_y_list, tail_x_list, tail_y_list

def get_start_position(row):
    start_positions = []

    for ind in row['stimulus_indices']:

        # print(ind)

        if ind > len(row['x']):
            # print('IND out of range')
            return start_positions

        start_positions.append([row['x'][ind], row['y'][ind]])

    return start_positions

def get_start_distance(row):
    start_distances = []

    for ind in row['stimulus_indices']:

        if ind > len(row['x']):
            print('IND out of range', row.name, ind)
            return start_distances

        start_distances.append(row['shelter_distance'][ind])

    return start_distances

def get_angle(row):
    x, y = row['x'], row['y']
    nest_coord = [0, 0]
    angles = np.arctan2(y - nest_coord[1], x - nest_coord[0])
    # coord_2[1] - coord_1[1], coord_2[0] - coord_1[0]
    return angles

def get_shelter_distance(row):
    dx, dy = (row['x'] - row['shelter_position'][0], row['y'] - row['shelter_position'][1])
    shelter_distances = np.sqrt(dx ** 2 + dy ** 2)

    return shelter_distances

def add_shelter_location(row):
    shelter_position = [0, 0]
    exp = row.name[:-1]
    if exp in nest_mean_dict:
        shelter_position = nest_mean_dict[exp]

    return shelter_position

def convert_coordinate_space(row):
    dist = 50
    conv_xy = []
    # start_distance = shelter
    # print('START ANGLE =')
    # print(row.name)
    for start_frame in row['stimulus_indices']:

        if start_frame > len(row['angles']):
            return conv_xy
        # print('start frame =', start_frame)
        # print(np.where(row['shelter_distance'][start_frame:-1] < dist))
        if len(np.where(row['shelter_distance'][start_frame:-1] < dist)[0]) == 0:
            print('DID NOT RETURN TO SHELTER')
            end_frame = -1
        elif len(np.where(row['shelter_distance'][start_frame:-1] < dist)[0]) != 0:
            end_frame = start_frame + np.where(row['shelter_distance'][start_frame:-1] < dist)[0][0]

        # print('end_frame =', end_frame)
        start_angle = row['angles'][start_frame]
        # print('START ANGLE =', start_angle)
        converted_x = row['shelter_distance'][start_frame:end_frame] * np.cos(
            np.pi / 2 + row['angles'][start_frame:end_frame] - start_angle)
        converted_y = row['shelter_distance'][start_frame:end_frame] * np.sin(
            np.pi / 2 + row['angles'][start_frame:end_frame] - start_angle)

        conv_xy.append([converted_x, converted_y])
    return conv_xy


def get_distance_travelled_before_flight(row):
    distances = []
    for ind in row['stimulus_indices']:

        # print(ind)
        if len(np.where(row['shelter_distance'][0:ind] < 50)[0]) == 0:
            continue
        prev_nest_frame = np.where(row['shelter_distance'][0:ind] < 50)[0][-1]

        distance_travelled_since_nest = sum(row['shelter_distance'][prev_nest_frame:ind])

        distances.append(distance_travelled_since_nest)

    return distances


def get_speed_change(row):
    return np.ediff1d(row['distance_per_frame'], to_begin=0)


def get_abs_speed_change_sum(row):
    return sum(np.absolute(row['speed_change']))


def get_flight_data(row, flight_dict, datatype, start_ind, end_ind):
    flight_dict[datatype] = row[datatype][start_ind:end_ind]
    return flight_dict


def populate_flight_dict(row, flight_dict):
    dist = 50  # distance cutoff for definition of 'in nest'
    pre_flight_window = 300  # in frames

    # Get name of experiment and set it as a variaBle ready to title ROw in df
    row_name = row.name
    print(row_name)

    experiment_name = row_name[:-1]
    experiment_subvid = row_name[-1]

    mouse_id = row['mouse_id']

    for i, ind in enumerate(row['stimulus_indices']):

        # Global index = place at which this flight will be entered into df (i.e. len of dict)
        global_index = str(len(flight_dict))

        # Create dict entry for flight
        flight_dict[global_index] = {}

        # Enter basic trial info
        flight_dict[global_index]['experiment_name'] = experiment_name
        flight_dict[global_index]['subvid'] = experiment_subvid
        flight_dict[global_index]['mouse_id'] = mouse_id
        flight_dict[global_index]['stimulus_index'] = ind

        try:
            if experiment_subvid == exp_info[experiment_name]['dwm_trial']:
                flight_dict[global_index]['dwm_trial'] = True

            elif experiment_subvid == exp_info[experiment_name]['dwm_trial']:
                flight_dict[global_index]['dwm_trial'] = False

            flight_dict[global_index]['expt_type'] = exp_info[experiment_name]['expt_type']

        except:
            print('Trial not in dicts')

        # Collect trials from the same session and create a count of them
        trial_num_count = 0
        for g_ind in flight_dict:
            if flight_dict[g_ind]['experiment_name'] == experiment_name:
                trial_num_count += 1

        flight_dict[global_index]['trial_num'] = trial_num_count

        # Find start index of trial
        flight_start_index = ind - pre_flight_window

        # Find the end index of the trial, set to -1 if not found. Logic:
        # 1) Find the point after the start index where distance to nest is greater than 'dist'
        # 2) If np.where returns nothing, set it to -1
        # 3) Otherwise get the index and add it to the start of flight to get index of end

        if len(np.where(row['shelter_distance'][ind:-1] < dist)[0]) == 0:
            flight_end_index = -1
        elif len(np.where(row['shelter_distance'][ind:-1] < dist)[0]) != 0:
            flight_end_index = ind + np.where(row['shelter_distance'][ind:-1] < dist)[0][0]

        data_to_move = ['x', 'y', 'head_x', 'head_y', 'tail_x', 'tail_y',
                        'angles', 'distance_per_frame', 'shelter_distance', 'vectors', 'speed_change']

        for dtype in data_to_move:
            flight_dict[global_index] = get_flight_data(
                row, flight_dict[global_index], dtype, flight_start_index, flight_end_index)

        if len(row['conv_xy']) - 1 >= i:

            if len(row['conv_xy']) > 0:
                print(i)
                flight_dict[global_index]['conv_xy'] = row['conv_xy'][i]

            elif len(row['conv_xy']) == 0:
                flight_dict[global_index]['conv_xy'] = []

        try:
            flight_dict[global_index]['distance_travelled_before'] = row['distance_travelled_before'][i]
        except:
            flight_dict[global_index]['distance_travelled_before'] = NaN

    return flight_dict


def get_flight_end_frame(row):
    row_name = row.name

def smooth_array(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def angle_between(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_angle_between_traj_points(row):
    v_pairs = zip(row['vectors'][1:], row['vectors'][:-1])
    vec_angles = []
    for pair in v_pairs:
        vec_angles.append(angle_between(pair[0], pair[1]))
    return vec_angles


def get_flight_dist_ratio(row):
    dist_ratio = False
    try:
        distance_travelled_in_flight = sum(row['distance_per_frame'][300:])
        start_distance = row['shelter_distance'][300]

        dist_ratio = distance_travelled_in_flight / start_distance

    except:
        ('Could not compute dist ratio. Ind may be out of range')
    return dist_ratio


def get_t_to_nest(row):
    return len(row['x'][300:])

def get_start_distance(row):
    try:
        d = row['shelter_distance'][300]
    except:
        d = 0
    return d


def get_flight_success(row, time_cutoff):
    min_speed = 0.5

    flight_categories = ['successful', 'unsuccessful', 'none']

    if len(row['x']) > time_cutoff:
        flight_success = flight_categories[1]

    elif len(row['x']) <= time_cutoff:
        flight_success = flight_categories[0]

    # if flight_success == 'unsuccessful':
    #    if row['distance_per_frame'].max() < min_speed:
    #        flight_success = flight_categories[2]

    return flight_success

