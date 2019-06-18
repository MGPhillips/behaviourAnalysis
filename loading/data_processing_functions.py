


def zeros_fun(arr):
    # Create an array that is 1 where arr is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(arr, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))

    # Runs start and end where absdiff is 1.
    zero_runs = np.where(absdiff == 1)[0].reshape(-1, 2)

    # Get sequences of zero coordinates and set first run equal to 1
    if len(zero_runs) != 0:

        start_zero_index1, start_zero_index2 = zero_runs[0][0], zero_runs[0][1]
        arr[start_zero_index1:start_zero_index2] = 1

        # Delete elements from zero_runs that are no longer zero
        np.delete(zero_runs, 0, 0)

        # Replace zeros
        for i in range(len(zero_runs)):
            if zero_runs[i][1] > (len(arr) - 1):
                return arr

            else:
                # Get indicies of the runs of zeros
                index1, index2 = zero_runs[i][0], zero_runs[i][1]

                # Get values of nearest non-zero values
                val1, val2 = arr[index1], arr[index2]

                # Get the length of the run
                len_run = index2 - index1

                # Smooth between two most recent non-zero points
                arr[index1:index2] = np.linspace(val1, val2, len_run)

    return arr


def fix_tracking(x, y, zeros_fun, distance_jump_limit):
    x = zeros_fun(x)
    y = zeros_fun(y)

    # Create array of distance travelled
    dist = np.zeros([len(x), 1])
    speed = np.zeros([len(x), 1])

    # Iterate through x
    for i in range(len(x)):
        if i < len(x) - 1:
            # Get distance between points
            dist[i] = (((x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2) ** .5)

            if dist[i] > distance_jump_limit:
                x[i + 1], y[i + 1] = x[i], y[i]

    return x, y
