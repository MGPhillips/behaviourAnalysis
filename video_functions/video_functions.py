

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



