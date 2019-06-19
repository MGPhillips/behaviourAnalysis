
import pandas as pd
from pylab import *
from analysis_functions import *

data_df['distance_per_frame'] = data_df.apply(get_speed, axis=1)
data_df['start_position'] = data_df.apply(get_start_position, axis=1)
data_df['angles'] = data_df.apply(get_angle, axis=1)
data_df['shelter_position'] = data_df.apply(add_shelter_location, axis=1)
data_df['shelter_distance'] = data_df.apply(get_shelter_distance, axis=1)
data_df['start_distance'] = data_df.apply(get_start_distance, axis=1)
data_df['conv_xy'] = data_df.apply(convert_coordinate_space, axis=1)
data_df['vectors'] = data_df.apply(get_vectors, axis=1)
data_df['distance_travelled_before'] = data_df.apply(get_distance_travelled_before_flight, axis=1)
data_df['speed_change'] = data_df.apply(get_speed_change, axis=1)

flight_dict = {}
flight_dict = data_df.apply(populate_flight_dict, args=(flight_dict,), axis=1)
flight_df = pd.DataFrame.from_dict(flight_dict[0], orient='index')

flight_df['speed_change'] = flight_df.apply(get_speed_change, axis=1)
flight_df['abs_speed_change_sum'] = flight_df.apply(get_abs_speed_change_sum, axis=1)
flight_df['flight_success'] = flight_df.apply(get_flight_success, args=(30 * 30,), axis=1)
flight_df['vec_angles'] = flight_df.apply(get_angle_between_traj_points, axis=1)
flight_df['flight_dist_ratio'] = flight_df.apply(get_flight_dist_ratio, axis=1)
flight_df['t_to_nest'] = flight_df.apply(get_t_to_nest, axis=1)
flight_df['start_distance'] = flight_df.apply(get_start_distance, axis=1)
