'''
Written by Kai Kun Xu
'''
"""
Link: https://github.com/huosan0123/quantile_normalization_python/blob/master/quantile_norm.py

The script is used to do quantile normalization.
The process is like R.preprocessCore.normalize.quantiles().  
Input data should be a np.ndarray or np.matrix type
return a same np.ndarray() type
"""
import numpy as np


def get_row_means(sorted_arr, rows, cols):
    """
    Given a dim=2 array, calculate its row means.
    As for Na, a float will be calculated by linear interpolation
    :param sorted_arr: sorted array of original arr. Na placed last on each column
    :param rows: rows of data, not counting header
    :param cols: rows of data, not counting header 
    :return: A new calloced row_means with size(rows) vector
    """
    eps = np.finfo(float).eps
    non_nas = rows - np.sum(np.isnan(sorted_arr), axis=0)
    row_means = np.zeros(rows, dtype=np.float64)

    for j in range(cols):
        non_na = non_nas[j]
        # if this column all is NA, skip. otherwise, row_means=nan, error
        if non_na == 0:
            continue
        
        if non_na == rows:
            for i in range(rows):
                row_means[i] += sorted_arr[i, j]

        else:
            for i in range(rows):
                sample_percent = float(i) / float(rows - 1)
                index_f = 1.0 + (non_na - 1.0) * sample_percent
                index_f_floor = np.floor(index_f + 4 * eps)
                index_f = index_f - index_f_floor

                if np.fabs(index_f <= 4 * eps):
                    index_f = 0.0

                if index_f == 0.0:
                    row_mean_id = int(np.floor(index_f_floor + 0.5))
                    row_means[i] += sorted_arr[row_mean_id - 1, j]
                elif index_f == 1.0:
                    row_mean_id = int(np.floor(index_f_floor + 1.5))
                    row_means[i] += sorted_arr[row_mean_id - 1, j]
                else:
                    row_mean_id = int(np.floor(index_f_floor + 0.5))

                    if row_mean_id < rows and row_mean_id > 0:
                        row_means[i] += (1.0 - index_f) * sorted_arr[row_mean_id-1, j] + \
                            index_f * sorted_arr[row_mean_id, j]
                    elif row_mean_id >= rows:
                        row_means[i] += sorted_arr[non_na - 1, j]
                    else:
                        row_means[i] += sorted_arr[0, j]
    row_means /= float(cols)
    return row_means


def get_ranks(sorted_arr, rows, cols):
    """
    sorted_arr is sorted in ascending order.
    rows, cols is its shape
    """
    ranks_arr = np.zeros((rows, cols), dtype=np.float64)
    ranks_arr[:, :] = np.NaN
    for c in range(cols):
        sorted_vec = sorted_arr[:, c]
        non_na = rows - np.sum(np.isnan(sorted_vec))

        i = 0
        while i < non_na:
            j = i
            # when meet ties, here after 5 lines do it.
            while j < non_na - 1 and sorted_vec[j] == sorted_vec[j+1]:
                j += 1
            if i != j:
                for k in range(i, j+1):
                    ranks_arr[k, c] = (i + j + 2.0) / 2.0
            else:
                ranks_arr[i, c] = i + 1
            i = j + 1

    return ranks_arr


def using_target(ranks_arr, index_arr, row_means, rows, cols):
    eps = np.finfo(float).eps
    non_nas = rows - np.sum(np.isnan(ranks_arr), axis=0)
    normed = np.zeros((rows, cols), dtype=np.float64)
    normed[:, :] = np.NaN

    for j in range(cols):
        non_na = non_nas[j]
        if non_na == rows:
            for i in range(rows):
                rank = ranks_arr[i, j]
                ori_i = index_arr[i, j]
                if rank - np.floor(rank) > 0.4:
                    normed[ori_i, j] = 0.5 * row_means[int(np.floor(rank)) - 1] + \
                        0.5 * row_means[int(np.floor(rank))]
                else:
                    normed[ori_i, j] = row_means[int(np.floor(rank)) - 1]
        else:
            for i in range(non_na):
                ori_i = index_arr[i, j]

                sample_percent = (ranks_arr[i, j] - 1.0) / float(non_na - 1)
                index_f = 1.0 + (rows - 1.0) * sample_percent
                index_f_floor = np.floor(index_f + 4 * eps)
                index_f -= index_f_floor

                if np.fabs(index_f) <= 4* eps:
                    index_f = 0.0

                if index_f == 0.0:
                    ind = int(np.floor(index_f_floor + 0.5))
                    normed[ori_i, j] = row_means[ind-1]
                elif index_f == 1.0:
                    ind = int(np.floor(index_f_floor + 1.5))
                    normed[ori_i, j] = row_means[ind-1]
                else:
                    ind = int(np.floor(index_f_floor + 0.5))
                    if (ind < rows) and ind > 0:
                        normed[ori_i, j] = (1.0 - index_f) * row_means[ind-1] + index_f * row_means[ind]
                    elif ind > rows:
                        normed[ori_i, j] = row_means[rows-1]
                    else:
                        normed[ori_i, j] = row_means[0]

    return normed


def quantile_normalize(input_arr):
    origin_arr = np.array(input_arr, dtype=np.float64)
    assert len(origin_arr.shape) == 2
    rows, cols = origin_arr.shape

    sorted_arr = np.sort(origin_arr, axis=0)
    ranks_arr = get_ranks(sorted_arr, rows, cols)
    row_means = get_row_means(sorted_arr, rows, cols)
    
    # index_arr is used to record the original position of origin arr.
    index_arr = np.argsort(origin_arr, axis=0)
    normed = using_target(ranks_arr, index_arr, row_means, rows, cols)

    return normed