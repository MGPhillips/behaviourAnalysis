

############### NOT READY YET -- COPY AND PASTED SEVERAL DIFFERENT BITS OF CODE HERE, SEPERATED BY ####

experiment = '190403_dwm_light_us_551_4a'
f = [x for x in h5_directories if experiment in x]

exp = f[0].split('\\')[-2]
vidpath = f[0].split('/')[0] + '\\cam1_FEC.avi'
print(vidpath)
print(experiment)
check_tracking(vidpath, 1000,
               data_df['x'][experiment],data_df['y'][experiment],
              data_df['head_x'][experiment],data_df['head_y'][experiment],
              data_df['tail_x'][experiment],data_df['tail_y'][experiment])

###################

clip_directories = []

for key in exp_info:
    bases.append(exp_info[key]['base_folder'] + '\\' + key)

for base in bases:
    for exc in to_exclude:
        if exc in base:
            continue

    clip_direct, filenames = get_filetype_paths('.avi', base)  # x, y, head_x, head_y, tail_x, tail_y

    clip_directories = clip_directories + clip_direct

to_strip = ['cam1', 'FEC', '_', '.avi', 'trackingcheck']

for clip in clip_directories:

    vid_name = clip.split('/')[-1]

    experiment_name = clip.split('/')[0].split('\\')[-1]

    if 'tracking_check' in vid_name:
        continue

    mouse_df = data_df[data_df.index == experiment_name]

    for ele in to_strip:
        vid_name = vid_name.replace(ele, '')

    if len(vid_name) == 0:
        continue
    print(experiment_name)
    stimulus_index = int(vid_name)

    output_name = 'tracking_check_' + vid_name

    produce_output_tracking_video(clip, output_name, stimulus_index, experiment_name, mouse_df)
#########################################
for key in exp_info:
    bases.append(exp_info[key]['base_folder'] + '\\' + key)

for base in bases:
    for exc in to_exclude:
        if exc in base:
            continue

    clip_direct ,filenames = get_filetype_paths('.avi', base)  # x, y, head_x, head_y, tail_x, tail_y

    clip_directories = clip_directories + clip_direct

to_strip = ['cam1', 'FEC', '_', '.avi', 'trackingcheck']

experiment_annotations = {}

for clip in clip_directories:

    vid_name = clip.split('/')[-1]

    experiment_name = clip.split('/')[0].split('\\')[-1]

    if 'tracking_check' not in vid_name:
        continue

    for ele in to_strip:
        vid_name = vid_name.replace(ele, '')

    if len(vid_name) == 0:
        continue
    print(experiment_name)
    stimulus_index = int(vid_name)

    output_name = 'tracking_check_' + vid_name

    experiment_annotations[vid_name] = annotate_tracking_videos(clip)

    prog = True

    while prog:

        progress = input('Progress to next exp? (y/n)')

        if progress in ['n', 'y']:
            break

    if progress == 'n':
        break

    if progress == 'y':
        continue





##########################


clip_path = 'E:\\Dropbox (UCL - SWC)\\big_Arena\\experiments\\dwm\\data\\basic\\180818_dwm_277_3\\180818_dwm_277_3a'

clip_directory, filenames = get_filetype_paths('.avi', clip_path)

for path in clip_directory:
    if path[-7:] != 'FEC.avi':
        continue
    experiment_name = path.split('/')[0].split('\\')[-1]

    exp_df = data_df[data_df.index == experiment_name]

    print(path)
    print(experiment_name)

    x, y, hx, hy, tx, ty = (
        exp_df['x'][0], exp_df['y'][0],
        exp_df['head_x'][0], exp_df['head_y'][0],
        exp_df['tail_x'][0], exp_df['tail_y'][0])

    check_tracking(path, '', 1, x, y, hx, hy, tx, ty)

    fix_x, fix_y, fix_hx, fix_hy, fix_tx, fix_ty =

