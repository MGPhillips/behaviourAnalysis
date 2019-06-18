

# TODO: Manage imports, setup exp info

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

data_dict = {}

data_dict = build_data_dict(data_dict, h5_directories, tdms_directories, exp_info)

data_df = pd.DataFrame.from_dict(data_dict, orient='index')



