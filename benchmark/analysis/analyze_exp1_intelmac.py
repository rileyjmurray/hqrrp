import numpy as np
from matplotlib import pyplot as plt


def read_data(threads):
    fname = f'../experiments/exp1_log_intelmac_{threads}threads.csv'
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


def plot_times(threads):
    data = read_data(threads)

    qrf = data[data[:, 4] == 'QRF', :][:, [0, 5]].astype(float)
    qrfx, qrfm, _ = mean_stddev(qrf[:, 0], qrf[:, 1])
    qp3 = data[data[:, 4] == 'QP3', :][:, [0, 5]].astype(float)
    qp3x, qp3m, _ = mean_stddev(qp3[:, 0], qp3[:, 1])
    qpr = data[data[:, 4] == 'QPR', :][:, [0, 5]].astype(float)
    qprx, qprm, _ = mean_stddev(qpr[:, 0], qpr[:, 1])
    plt.plot(qrfx, qrfm, c='b')
    plt.plot(qprx, qprm, c='k')
    plt.plot(qp3x, qp3m, c='r')
    plt.legend(['QRF', 'QPR', 'QP3'])
    plt.title(f'Runtimes (ms) for Intel mac ({threads} threads)')
    plt.show()

    ratf = qp3[:, 1] / qrf[:, 1]
    rat4 = qp3[:, 1] / qpr[:, 1]
    ratfx, ratfm, ratfs = mean_stddev(qp3[:, 0], ratf)
    rat4x, rat4m, rat4s = mean_stddev(qp3[:, 0], rat4)
    plt.errorbar(ratfx, ratfm, yerr=ratfs, c='b')
    plt.errorbar(rat4x, rat4m, yerr=rat4s, c='k')
    plt.legend(['QP3 / QRF', 'QP3 / QPR'])
    plt.title(f'Speedups over QP3 for Intel mac ({threads} threads)')
    plt.show()


def effective_gflops_square(sizes, times):
    num = (sizes * 1e-3)**3
    num *= 4/3
    gflops = num / (times/1000)
    return gflops


def plot_flop_rates(threads):
    data = read_data(threads)
    qrf = data[data[:, 4] == 'QRF', :][:, [0, 5]].astype(float)
    qrfx, qrfm, _ = mean_stddev(qrf[:, 0], qrf[:, 1])
    qp3 = data[data[:, 4] == 'QP3', :][:, [0, 5]].astype(float)
    qp3x, qp3m, _ = mean_stddev(qp3[:, 0], qp3[:, 1])
    qpr = data[data[:, 4] == 'QPR', :][:, [0, 5]].astype(float)
    qprx, qprm, _ = mean_stddev(qpr[:, 0], qpr[:, 1])
    plt.plot(qrfx, effective_gflops_square(qrfx, qrfm), c='b')
    plt.plot(qprx, effective_gflops_square(qprx, qprm), c='k')
    plt.plot(qp3x, effective_gflops_square(qp3x, qp3m), c='r')
    plt.legend(['QRF', 'QPR', 'QP3'])
    plt.ylabel('GFlops')
    plt.xlabel('n')
    plt.title(f'Standardized GFlops for Intel mac ({threads} threads)')
    plt.show()
    pass


if __name__ == '__main__':
    plot_times(2)
    plot_flop_rates(2)
    plot_times(4)
    plot_flop_rates(4)

