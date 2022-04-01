import numpy as np


def read_exp1_data(platform, threads):
    if isinstance(threads, int):
        fname = f'../experiments/exp1_log_{platform}_{threads}threads.csv'
    else:
        assert threads == ''
        fname = f'../experiments/exp1_log_{platform}_accel.csv'
    data = np.genfromtxt(fname, dtype=object, delimiter=',')
    data[:, 0] = data[:, 0].astype(int)
    data[:, 1] = data[:, 1].astype(int)
    data[:, 2] = np.array([s.strip() for s in data[:, 2].astype(str)])
    data[:, 3] = data[:, 3].astype(int)
    data[:, 4] = np.array([s.strip() for s in data[:, 4].astype(str)])
    data[:, 5] = data[:, 5].astype(float)
    return data


def mean_stddev(x, y):
    ux = np.unique(x)
    means = np.zeros(ux.size)
    stddevs = np.zeros(ux.size)
    for i, val in enumerate(ux):
        yi = y[x == val]
        means[i] = np.mean(yi)
        stddevs[i] = np.std(yi)
    return ux, means, stddevs


def exp1_times_means_and_stddevs(data):
    qrf = data[data[:, 4] == 'QRF', :][:, [0, 5]].astype(float)
    qp3 = data[data[:, 4] == 'QP3', :][:, [0, 5]].astype(float)
    qpr = data[data[:, 4] == 'QPR', :][:, [0, 5]].astype(float)
    qrf = mean_stddev(qrf[:, 0], qrf[:, 1])
    qp3 = mean_stddev(qp3[:, 0], qp3[:, 1])
    qpr = mean_stddev(qpr[:, 0], qpr[:, 1])
    return qrf, qp3, qpr


def exp1_ratio_means_and_stddevs(data):
    qrf = data[data[:, 4] == 'QRF', :][:, [0, 5]].astype(float)
    qp3 = data[data[:, 4] == 'QP3', :][:, [0, 5]].astype(float)
    qpr = data[data[:, 4] == 'QPR', :][:, [0, 5]].astype(float)
    ratf = qp3[:, 1] / qrf[:, 1]
    ratr = qp3[:, 1] / qpr[:, 1]
    qrf = mean_stddev(qrf[:, 0], ratf)
    qpr = mean_stddev(qpr[:, 0], ratr)
    return qrf, qpr


def exp1_floprates_means_and_stddevs(data):
    qrf = data[data[:, 4] == 'QRF', :][:, [0, 5]].astype(float)
    qp3 = data[data[:, 4] == 'QP3', :][:, [0, 5]].astype(float)
    qpr = data[data[:, 4] == 'QPR', :][:, [0, 5]].astype(float)
    qrf[:, 1] = effective_gflops_square(qrf[:, 0], qrf[:, 1])
    qpr[:, 1] = effective_gflops_square(qpr[:, 0], qpr[:, 1])
    qp3[:, 1] = effective_gflops_square(qp3[:, 0], qp3[:, 1])
    qrf = mean_stddev(qrf[:, 0], qrf[:, 1])
    qp3 = mean_stddev(qp3[:, 0], qp3[:, 1])
    qpr = mean_stddev(qpr[:, 0], qpr[:, 1])
    return qrf, qp3, qpr


def effective_gflops_square(sizes, times):
    num = (sizes * 1e-3)**3
    num *= 4/3
    gflops = num / (times/1000)
    return gflops
