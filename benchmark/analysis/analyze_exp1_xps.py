import numpy as np
from matplotlib import pyplot as plt


def read_data():
    data = np.genfromtxt('../exp1_log_xps.csv', dtype=object, delimiter=',')
    data[:, 0] = data[:, 0].astype(int)
    data[:, 1] = data[:, 1].astype(int)
    data[:, 2] = np.array([s.strip() for s in data[:, 2].astype(str)])
    data[:, 3] = data[:, 3].astype(int)
    data[:, 4] = np.array([s.strip() for s in data[:, 4].astype(str)])
    col4 = data[:, 4]
    col4[col4 == 'QP4'] = 'QPR'
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


if __name__ == '__main__':
    data = read_data()

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
    plt.show()

    ratf = qp3[:, 1] / qrf[:, 1]
    rat4 = qp3[:, 1] / qpr[:, 1]
    ratfx, ratfm, ratfs = mean_stddev(qp3[:, 0], ratf)
    rat4x, rat4m, rat4s = mean_stddev(qp3[:, 0], rat4)
    plt.errorbar(ratfx, ratfm, yerr=ratfs, c='b')
    plt.errorbar(rat4x, rat4m, yerr=rat4s, c='k')
    plt.legend(['QP3 / QRF', 'QP3 / QPR'])
    plt.show()

    qpr_unif = data[(data[:, 4] == 'QPR') & (data[:, 2] == 'u'), :][:, [0, 5]].astype(float)
    qp3_unif = data[(data[:, 4] == 'QP3') & (data[:, 2] == 'u'), :][:, [0, 5]].astype(float)
    qpr_norm = data[(data[:, 4] == 'QPR') & (data[:, 2] == 'n'), :][:, [0, 5]].astype(float)
    qp3_norm = data[(data[:, 4] == 'QP3') & (data[:, 2] == 'n'), :][:, [0, 5]].astype(float)

    ratu = qp3_unif[:, 1] / qpr_unif[:, 1]
    ratn = qp3_norm[:, 1] / qpr_norm[:, 1]
    ratux, ratum, ratus = mean_stddev(qp3_unif[:, 0], ratu)
    ratnx, ratnm, ratns = mean_stddev(qp3_norm[:, 0], ratn)
    plt.errorbar(ratux, ratum, yerr=ratus)
    plt.errorbar(ratnx, ratnm, yerr=ratns)
    plt.legend(['QP3 / QPR : uniform', 'QP3 / QPR : normal'])
    plt.show()
