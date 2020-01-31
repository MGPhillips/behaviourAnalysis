import cv2
from tqdm import tqdm
import csv
import os.path
from os import path
import ast


import sys
sys.path.insert(0, r'C:\Users\matthewp.W221N\Documents\GitHub\behaviourAnalysisMP\loading')

#from load_data import *
from load_functions import *


save_out_path = r'C:\Users\matthewp.W221N\Desktop\nest_positions_dwm.csv'

def load_csv_to_nest_dict(path):

    # Load data
    nest_data = csv.DictReader(open(path))

    # Create output dict
    d = {}

    # Cycle through the dictreader object and sort into a dict of the correct format
    for row in nest_data:

        # row comes out in a strange format -- it takes the first row as headers, second row as a list entry
        # However, we want multiple rows -- need to do some logic and convert from string formats to get this correct

        for key in row:
            # Convert from string format to list
            dict_entry = ast.literal_eval(row[key])

            # See if we already stored a value from this key - if yes, add to it, if no, create it
            if key in d:
                d[key] += [dict_entry]

            elif key not in d:
                d[key] = [dict_entry]

    return d

def save_out_nest_positions(path, nest_dict):

    with open(path, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(nest_dict.keys())
        writer.writerows(zip(*nest_dict.values()))

def get_background(vidpath, start_frame=1000, avg_over=100):
    vid = cv2.VideoCapture(vidpath)

    # initialize the video
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    background = np.zeros((height, width))
    num_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # initialize the counters
    every_other = int(num_frames / avg_over)
    j = 0

    for i in tqdm(range(num_frames)):

        if i % every_other == 0:
            vid.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = vid.read()  # get the frame

            if ret:
                # store the current frame in as a numpy array
                background += frame[:, :, 0]
                j += 1

    background = (background / (j)).astype(np.uint8)
    cv2.imshow('Vid Background', background)
    cv2.waitKey(10)
    vid.release()

    return background

def draw_circle(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDBLCLK:

        print('button clicked at',x,y)
        param.append([x, y])
        print('Param:', param)
        cv2.circle(img, (x, y), 4, (255, 0, 0), -1)

def annotate_nest(nest_dict, h5_directories):

    # nest_dict = {}

    for f in h5_directories:
        cv2.destroyAllWindows()
        #while True:
        #    inp = input('Progress? (type y)')

         #   if inp == 'y':
         #       break



        exp = f.split('\\')[-2]

        print('Progressing to: ', exp)

        if exp in nest_dict:
            print(exp, '... completed already')
            continue

        print('Loading...', exp)

        vidpath = f.split('/')[0] + '\\cam1_FEC.avi'

        img = get_background(vidpath, 1000, 100)

        print('\nSelect reference points on the image window')
        print('First select the entrance, then each corner going clockwise')

        nest_points = []

        # initialize GUI
        # cv2.startWindowThread()

        # FIRST POINT: ENTRANCE, THEN GO CLOCKWISE (FRONT RIGHT, BACK RIGHT etc)
        number_clicked_points = 0
        cv2.namedWindow('image')

        # create functions to react to clicked points
        cv2.setMouseCallback('image', draw_circle, nest_points)  # Mouse callback

        while (1):

            cv2.imshow('image', img)
            #print(nest_points)
            if len(nest_points) == 5:
                b_query = input('Is this correct? (y/n)')
                if b_query == 'y':
                    break

                if b_query != 'y':
                    cv2.destroyAllWindows()

            if cv2.waitKey(ord('y')) & 0xFF == 27:
                break

        nest_dict[exp] = nest_points

    return nest_dict

exp_info = {}
#exp_info_path = 'E:\\big_arena_analysis\\dwm_darklight_analysis.csv'
#exp_info_path = 'E:\\big_arena_analysis\\hc_lesion_analysis.csv'
#exp_info_path = 'E:\\big_arena_analysis\\mouse_rotation_analysis.csv'
exp_info_path = 'E:\\big_arena_analysis\\dwm_trial_analysis.csv'

exp_info = populate_exp_info(exp_info, exp_info_path)

to_exclude = ['180402_longrange_nowall_2a', '180402_longrange_nowall_3a', '180422_dwm_240_2a',
              '18MAY15_2404_DM', '18MAY15_2404_DM', '18MAY15_2403_DM','190528_mouserotation_dark_677_1']

h5_directories, tdms_directories = get_directories(exp_info, to_exclude)

DLC_networks = ['cam1_FECDeepCut_resnet50_phillips_mg_800000']

h5_directories = [x for x in h5_directories if DLC_networks[0] in x]


if path.exists(save_out_path):

    nest_dict = load_csv_to_nest_dict(save_out_path)

elif not path.exists(save_out_path):
    nest_dict = {}

print('entering nest annotation')
nest_dict = annotate_nest(nest_dict, h5_directories)

save_out_nest_positions(save_out_path, nest_dict)

#with open(r'C:\Users\matthewp.W221N\Desktop\nest_positions_mouse_rotation1.csv', 'w') as f:
#    for key in nest_dict.keys():
#        f.write("%s,%s\n"%(key, nest_dict[key]))


