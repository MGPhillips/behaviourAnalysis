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
        cv2.circle(img, (x, y), 4, (255, 0, 0), -1)

        param.append([x, y])


def annotate_nest(nest_dict, h5_directories):

    # nest_dict = {}

    for f in h5_directories:
        cv2.destroyAllWindows()
        while True:
            inp = input('Progress? (type y)')

            if inp == 'y':
                break

        exp = f.split('\\')[-2]

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


def check_tracking(vid_path, output_name, start_frame, x, y, head_x, head_y, tail_x, tail_y):
    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # CV_
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    time_length = fps * frameCount

    frame_no = (start_frame / (time_length * fps))

    count = 0
    cv2.namedWindow("Tracking check", cv2.WINDOW_AUTOSIZE)

    label_dict = {}

    while cap.isOpened():

        # Read video capture
        ret, frame = cap.read()

        # Display each frame
        cv2.circle(frame, (int(x[count]), int(y[count])), 4, (255, 0, 0), -1)

        cv2.circle(frame, (int(head_x[count]), int(head_y[count])), 4, (0, 255, 0), -1)
        cv2.circle(frame, (int(tail_x[count]), int(tail_y[count])), 4, (0, 0, 255), -1)

        img = cv2.imshow("Tracking check", frame)

        # show one frame at a time
        count += 1
        key = cv2.waitKey(0)
        if (count + start_frame) % 100 == 0:
            print('Frame', count + start_frame, 'reached')
        while key not in [ord('q'), ord('k')]:
            key = cv2.waitKey(0)

        # Quit when 'q' is pressed
        if key == ord('q'):
            break

    # Release capture object
    cap.release()

    # Exit and distroy all windows
    cv2.destroyAllWindows()


def annotate_tracking_videos(vid_path):
    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # CV_
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    count = 0
    error_count = 0

    ### Annotations:
    # r = reaction to stimulus -- NOT FUNCTIONAL
    # t = body tracking broken
    # h = head/tail flipped
    # f = failed flight
    # s = succesful flight
    # c = clear all entries for this frame

    annotations = {  # 'r': [],
        't': False,
        'h': False,
        'f': False,
        's': False,
        'c': False}

    while cap.isOpened():

        # Read video capture
        ret, frame = cap.read()
        try:
            img = cv2.imshow("Tracking check", frame)
        except:
            print('End at frame...', count)
            return annotations
        # show one frame at a time
        count += 1
        key = cv2.waitKey(0)

        if count % 100 == 0:
            print('Frame', count, 'reached')

        # print(key)
        if key is not -1:

            if chr(key) in annotations:
                annotations[chr(key)] = True

        while key not in [ord('q'), ord('k')] + [ord(x) for x in annotations]:
            key = cv2.waitKey(0)

        # Quit when 'q' is pressed
        if key == ord('q'):
            break
        # else:
        #    break

    # Release capture object
    cap.release()

    # Exit and distroy all windows
    cv2.destroyAllWindows()

    return annotations


def produce_output_tracking_video(vid_path, output_name, stim_frame, experiment_name, data_df):
    try:
        data_df['x'][experiment_name]
    except:
        return

    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # CV_
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    time_length = fps * frameCount

    ## Adding 100 secs of tracking data as video lens may vary
    window = fps * 120

    start_frame = int(stim_frame)
    end_frame = int(stim_frame + window)

    # frame_no = (start_frame /(time_length*fps))

    # cap.set(2,frame_no);

    path = vid_path.split('/')[0]

    out_string = path + '//' + output_name + '.avi'
    # fourcc = cv2.VideoWriter_fourcc(*"XVID")

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(out_string, fourcc, fps, (width, height))

    print('outstring =', out_string)

    x, y, head_x, head_y, tail_x, tail_y = (
        data_df['x'][experiment_name][start_frame:end_frame], data_df['y'][experiment_name][start_frame:end_frame],
        data_df['head_x'][experiment_name][start_frame:end_frame],
        data_df['head_y'][experiment_name][start_frame:end_frame],
        data_df['tail_x'][experiment_name][start_frame:end_frame],
        data_df['tail_y'][experiment_name][start_frame:end_frame])

    count = 0
    error_count = 0
    while cap.isOpened():

        # Read video capture
        ret, frame = cap.read()
        if ret == True:
            if count == 0:
                print('Entering video production')
            # Display each frame
            try:
                cv2.circle(frame, (int(x[count]), int(y[count])), 4, (255, 0, 0), -1)
                cv2.circle(frame, (int(head_x[count]), int(head_y[count])), 4, (0, 255, 0), -1)
                cv2.circle(frame, (int(tail_x[count]), int(tail_y[count])), 4, (0, 0, 255), -1)
            except:
                if error_count == 0:
                    print('Could not plot')

            out.write(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            count += 1

        else:
            break

    # Release capture object
    cap.release()
    out.release()

    # Exit and distroy all windows
    cv2.destroyAllWindows()


avi_paths = get_filetype_paths('.avi',
                               r'E:\Dropbox (UCL - SWC)\big_Arena\experiments\dwm\data\basic') + get_filetype_paths(
    '.avi', r'E:\Dropbox (UCL - SWC)\big_Arena\experiments\dwm\data\dark')
fdf_paths = {}

for p in avi_paths:

    if 'FEC' in p:

        if p[-7:] == 'FEC.avi':
            continue

        if 'tracking' in p:
            continue

        split = p.split('\\')

        expt_name = split[-3]
        subfolder = split[-2][-1]
        trial = split[-1]

        trial = trial.replace('cam1_FEC_', '')
        trial = trial.replace('.avi', '')

        print(expt_name, trial)

        inds = flight_df[
            (flight_df['experiment_name'] == expt_name) & (flight_df['stimulus_index'] == int(trial) + 900)].index

        if len(inds) > 0:

            fdf_paths[expt_name + '/' + str(trial)] = p

        else:
            print('No entry for path:', p)


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def produce_output_tracking_video(vid_path, output_name, stim_frame, experiment_name, data_df,
                                  save_labeled_frames=False):
    try:
        data_df['x'][experiment_name]
    except:
        print('Failure in data_df')
        return

    cap = cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # CV_
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    time_length = fps * frameCount

    ## Adding 100 secs of tracking data as video lens may vary
    window = fps * 120

    start_frame = int(stim_frame - 30 * fps)
    end_frame = int(start_frame + frameCount)

    # frame_no = (start_frame /(time_length*fps))

    # cap.set(2,frame_no);

    # path = vid_path.split('/')[0]

    out_string = vid_path.replace(path.split('\\')[-1], '') + output_name + '.avi'
    # fourcc = cv2.VideoWriter_fourcc(*"XVID")

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(out_string, fourcc, fps, (width, height))

    print('outstring =', out_string)

    x, y, head_x, head_y, tail_x, tail_y = (
        data_df['x'][experiment_name][start_frame:end_frame], data_df['y'][experiment_name][start_frame:end_frame],
        data_df['head_x'][experiment_name][start_frame:end_frame],
        data_df['head_y'][experiment_name][start_frame:end_frame],
        data_df['tail_x'][experiment_name][start_frame:end_frame],
        data_df['tail_y'][experiment_name][start_frame:end_frame])

    count = 0
    error_count = 0

    plot_series_x = []
    plot_series_y = []

    frame_dir = path + '\\frames\\' + str(stim_frame)

    while cap.isOpened():

        # Read video capture
        ret, frame = cap.read()
        if ret == True:
            if count == 0:
                print('Entering video production for ', out_string)
            # Display each frame

            if save_labeled_frames:

                out_frame = plt.imshow(frame)
                out_frame = plt.plot(x[0:count], y[0:count])
                out_frame = plt.scatter(x[count], y[count], alpha=0.5, s=1, color='navy')

                if not os.path.exists(frame_dir):
                    os.makedirs(frame_dir)

                frame_out_path = frame_dir + '\\frame_' + str(count)
                out_frame.savefig(frame_out_path)

            try:
                cv2.circle(frame, (int(x[count]), int(y[count])), 4, (255, 0, 0), -1)
                cv2.circle(frame, (int(head_x[count]), int(head_y[count])), 4, (0, 255, 0), -1)
                cv2.circle(frame, (int(tail_x[count]), int(tail_y[count])), 4, (0, 0, 255), -1)

            except:
                if error_count == 0:
                    print('Could not plot')

            out.write(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            count += 1

        else:
            break

    # Release capture object
    cap.release()
    out.release()

    # Exit and distroy all windows
    cv2.destroyAllWindows()


dark_base = r'E:\Dropbox (UCL - SWC)\big_Arena\experiments\dwm\data\dark'
light_base = r'E:\Dropbox (UCL - SWC)\big_Arena\experiments\dwm\data\basic'

# dark_paths = get_filetype_paths('.avi', dark_base)
# light_paths = get_filetype_paths('.avi', light_base)
fec_paths = get_filetype_paths('.avi', light_base)  # dark_paths + light_paths

# fec_paths, _ = get_filetype_paths('.avi', dark_base)
# fec_paths, _ += get_filetype_paths('.avi', light_base)
for path in fec_paths:

    experiment_name = path.split('\\')[-2]  # .split('/')[0]
    print(experiment_name)
    if len(data_df[data_df.index == experiment_name]['stimulus_indices']) == 0:
        continue

    if 'cam1_FEC_' not in path.split('\\')[-1]:
        print('skipping... not a trial video')
        continue
    stims = data_df[data_df.index == experiment_name]['stimulus_indices'][0]  # .items
    print(stims)

    print(path)
    expt_name = path.split('\\')[-2]
    trial = path.split('\\')[-1]
    trial = trial.replace('cam1_FEC_', '')
    trial = trial.replace('.avi', '')
    trial = int(trial)

    stims = data_df[data_df.index == expt_name]['stimulus_indices'].values[0]
    stim = int(find_nearest(stims, trial))

    output_name = 'newnet_tracking_check_stim_' + str(stim)
    produce_output_tracking_video(path, output_name, stim, experiment_name, data_df)


def get_video_frames(loadpath, savepath, frames, key):
    # Takes a video path and returns images of the frames given in the list 'frames'
    # loadpath: path to desired video
    # frames: list of desired frames
    folder_path = savepath.replace(savepath.split('\\')[-1], '')
    print('Folder path:', folder_path)

    trial = key.split('/')[-1]
    print('Trial:', trial)

    cap = cv2.VideoCapture(loadpath)

    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    count = 0

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if length / fps != 60:
        print('length too short for:', loadpath)
        return

    # cap.set(cv2.CV_CAP_PROP_POS_FRAMES,start_frame/length) #cv2.CV_CAP_PROP_POS_FRAMES,
    try:
        os.mkdir(folder_path + "frames_" + trial)
    except:
        print('Folder exists. Continuing to save..')

    for frame_n in frames:
        cap = cv2.VideoCapture(loadpath)

        if (cap.isOpened() == False):
            print("Unable to read camera feed")

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_n)

        while cap.isOpened():
            ret, frame = cap.read()

            saveout_path = folder_path + '\\' + 'frames_' + trial + "\\frame_" + trial + "_%d.jpg" % frame_n

            cv2.imwrite(saveout_path, frame)
            # cv2.imshow("video", frame)

            cap.release()
            # Closes all the frames
            cv2.destroyAllWindows()

    # except:
    #   print('Failed! Moving on...')

    # cap.release()
    # Closes all the frames
    # cv2.destroyAllWindows()

    return


frames = np.linspace(600, 1200, 101)
# frames = [0, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700]

# print(save_path)

# load_path = fdf_paths[list(fdf_paths)[-1]]
# save_path = fdf_paths[list(fdf_paths)[-1]].replace(load_path.split('\\')[-1], '')

for key in fdf_paths:
    load_path = fdf_paths[key]
    save_path = fdf_paths[key.replace(load_path.split('\\')[-1], '')]
    print('Saving frames from:', key)
    get_video_frames(load_path, save_path, frames, key)


def make_overlay(loadpath, savepath, frames, key):
    # Takes a video path and returns images of the frames given in the list 'frames'
    # loadpath: path to desired video
    # frames: list of desired frames
    folder_path = savepath.replace(savepath.split('\\')[-1], '')
    print('Folder path:', folder_path)

    trial = key.split('/')[-1]
    print('Trial:', trial)

    cap = cv2.VideoCapture(loadpath)

    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    count = 0

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if length / fps != 60:
        print('length too short for:', loadpath)
        return

    # cap.set(cv2.CV_CAP_PROP_POS_FRAMES,start_frame/length) #cv2.CV_CAP_PROP_POS_FRAMES,
    try:
        os.mkdir(folder_path + "frames_" + trial)
    except:
        print('Folder exists. Continuing to save..')

    for frame_n in frames:
        cap = cv2.VideoCapture(loadpath)

        if (cap.isOpened() == False):
            print("Unable to read camera feed")

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_n)

        while cap.isOpened():
            ret, frame = cap.read()

            saveout_path = folder_path + '\\' + 'frames_' + trial + "\\frame_" + trial + "_%d.jpg" % frame_n

            cv2.imwrite(saveout_path, frame)
            # cv2.imshow("video", frame)

            cap.release()
            # Closes all the frames
            cv2.destroyAllWindows()

    # except:
    #   print('Failed! Moving on...')

    # cap.release()
    # Closes all the frames
    # cv2.destroyAllWindows()

    return


frames = np.linspace(600, 1200, 101)
# frames = [0, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700]

# print(save_path)

# load_path = fdf_paths[list(fdf_paths)[-1]]
# save_path = fdf_paths[list(fdf_paths)[-1]].replace(load_path.split('\\')[-1], '')

for key in fdf_paths:
    load_path = fdf_paths[key]
    save_path = fdf_paths[key.replace(load_path.split('\\')[-1], '')]
    print('Saving frames from:', key)
    get_video_frames(load_path, save_path, frames, key)



def get_background(vidpath, start_frame = 1000, avg_over = 100):
    """ extract background: average over frames of video """

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
                j+=1


    background = (background / (j)).astype(np.uint8)
    cv2.imshow('background', background)
    cv2.waitKey(10)
    vid.release()

    return background

bg = get_background(fdf_paths[list(fdf_paths)[-1]])


def get_brightness(f):
    img = (f[..., 0] + f[..., 1] + f[..., 2]) / 3

    return img


def get_background(fs):
    avg = sum([f for f in fs])
    avg = avg / len(fs)
    return


bs = []

for f in fs:
    bs.append(get_brightness(f))

# b_img = np.zeros(np.shape(bs[0]))

# for b in bs:
#    plt.imshow(b-bg,)
#    b_img -= b


fig = plt.figure(figsize=(8, 8))
cols = 3
rows = 1

for i in range(1, cols * rows + 1):
    fig.add_subplot(rows, cols, i)

    # print(np.shape(bg), np.shape(bs[i-1]))

    # bg_img = get_brightness(bg)
    # bs_img = get_brightness(bs[i-1])

    print(np.shape(bs[i - 1]), np.shape(bg))

    plt.imshow(bs[i - 1] - bg, cmap='gray')
    # plt.imshow(bs[i-1]-bg)

plt.show()


def get_frame_scatter(loadpath, savepath, df, frames):
    frame = get_single_frame(loadpath, frame_ind)
    expt =
    stimulus_index =

    x = df[]

    fig = plt.imshow(frame)

    fig = plt.scatter()


def get_single_frame(videopath, frame_number):
    cap = cv2.VideoCapture(videopath)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()

    return frame


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def produce_tracked_frame(load_path, save_path,
                          data_df, frames, track_color):
    folder_path = save_path.replace(save_path.split('\\')[-1], '')
    for ind, i in enumerate(frames):  # ,1000,1100]:

        plt.clf()

        # load_path = fdf_paths[list(fdf_paths)[-1]]
        try:
            f = get_single_frame(load_path, i)

            expt_name = load_path.split('\\')[-2]
            trial = load_path.split('\\')[-1]
            trial = trial.replace('cam1_FEC_', '')
            trial = trial.replace('.avi', '')
            trial = int(trial)

            stims = data_df[data_df.index == expt_name]['stimulus_indices'].values[0]
            stim = int(find_nearest(stims, trial))

            x, y = data_df[data_df.index == expt_name]['x'][0][stim:stim + int(i) - 900], \
                   data_df[data_df.index == expt_name]['y'][0][stim:stim + int(i) - 900]

            fig = plt.imshow(f)

            fig = plt.scatter(x, y, s=2, color=track_color, alpha=0.5)

            plt.axis('off')

            # saveout_path = folder_path + '\\' + 'frames_' + str(trial) + "\\frame_" + str(trial) + "_%d.jpg" % frame_n

            try:
                os.mkdir(folder_path + "frames_" + trial)
            except:
                print('Folder exists. Continuing to save..')

            saveout_path = folder_path + 'frames_' + str(trial) + "\\frame_tracked_" + str(trial) + "_%d.jpg" % i

            plt.savefig(saveout_path)

        except:
            print('Could not produce tracking image for:', load_path)


frames = np.linspace(900, 1200, 61)
# frames = [0, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700]

# print(save_path)

# load_path = fdf_paths[list(fdf_paths)[-1]]
# save_path = fdf_paths[list(fdf_paths)[-1]].replace(load_path.split('\\')[-1], '')

for key in fdf_paths:
    load_path = fdf_paths[key]
    save_path = fdf_paths[key.replace(load_path.split('\\')[-1], '')]
    print(load_path)
    # print(data_df[data_df.index==load_path.split('\\')[-2]]['experiment_type'][0])
    track_color = colors[data_df[data_df.index == load_path.split('\\')[-2]]['experiment_type'][0]]
    produce_tracked_frame(load_path, save_path, data_df, frames, track_color)


def produce_tracked_frame_for_overlay(load_path, save_path, data_df, frames, track_colors):
    folder_path = save_path.replace(save_path.split('\\')[-1], '')

    for ind, i in enumerate(frames):  # ,1000,1100]:

        plt.clf()

        # load_path = fdf_paths[list(fdf_paths)[-1]]
        try:
            f = get_single_frame(load_path, i)

            expt_name = load_path.split('\\')[-2]
            trial = load_path.split('\\')[-1]
            trial = trial.replace('cam1_FEC_', '')
            trial = trial.replace('.avi', '')
            trial = int(trial)

            stims = data_df[data_df.index == expt_name]['stimulus_indices'].values[0]
            stim = int(find_nearest(stims, trial))

            x, y = (data_df[data_df.index == expt_name]['x'][0][stim + int(i) - 900],
                    data_df[data_df.index == expt_name]['y'][0][stim + int(i) - 900])

            head_x, head_y = (data_df[data_df.index == expt_name]['head_x'][0][stim + int(i) - 900],
                              data_df[data_df.index == expt_name]['head_y'][0][stim + int(i) - 900])

            tail_x, tail_y = (data_df[data_df.index == expt_name]['tail_x'][0][stim + int(i) - 900],
                              data_df[data_df.index == expt_name]['tail_y'][0][stim + int(i) - 900])
            fig = plt.imshow(f)

            fig = plt.scatter(x, y, s=2, color=track_color, alpha=0.5)
            fig = plt.scatter(head_x, head_y, s=2, color=track_color, alpha=0.5)
            fig = plt.scatter(tail_x, tail_y, s=2, color=track_color, alpha=0.5)
            plt.axis('off')

            # saveout_path = folder_path + '\\' + 'frames_' + str(trial) + "\\frame_" + str(trial) + "_%d.jpg" % frame_n

            try:
                os.mkdir(folder_path + "frames_" + trial)
            except:
                print('Folder exists. Continuing to save..')

            saveout_path = folder_path + 'frames_' + str(trial) + "\\frame_DLCpoints_" + str(trial) + "_%d.jpg" % i

            plt.savefig(saveout_path)

        except:
            print('Could not produce tracking image for:', load_path)


frames = np.linspace(900, 1200, 61)
# frames = [0, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700]

# print(save_path)

# load_path = fdf_paths[list(fdf_paths)[-1]]
# save_path = fdf_paths[list(fdf_paths)[-1]].replace(load_path.split('\\')[-1], '')
track_colors = ['m', 'violet', 'darkmagenta']
for key in fdf_paths:
    load_path = fdf_paths[key]
    save_path = fdf_paths[key.replace(load_path.split('\\')[-1], '')]
    print(load_path)
    # print(data_df[data_df.index==load_path.split('\\')[-2]]['experiment_type'][0])
    # track_color = colors[data_df[data_df.index==load_path.split('\\')[-2]]['experiment_type'][0]]
    produce_tracked_frame_for_overlay(load_path, save_path, data_df, frames, track_colors)
