import numpy as np
from matplotlib import pyplot as plt
import analysis.helpers as helpers


def plot_times(threads):
    data = helpers.read_exp1_data('xps', threads)
    qrf, qp3, qpr = helpers.exp1_times_means_and_stddevs(data)
    plt.plot(qrf[0], qrf[1], c='b')
    plt.plot(qpr[0], qpr[1], c='k')
    plt.plot(qp3[0], qp3[1], c='r')
    plt.legend(['QRF', 'QPR', 'QP3'])
    plt.title(f'Runtimes (ms) for XPS 9300 ({threads} threads)')
    plt.show()


def plot_speedups(threads):
    data = helpers.read_exp1_data('xps', threads)
    ratf, ratr = helpers.exp1_ratio_means_and_stddevs(data)
    plt.errorbar(ratf[0], ratf[1], yerr=ratf[2], c='b')
    plt.errorbar(ratr[0], ratr[1], yerr=ratr[2], c='k')
    plt.legend(['QRF', 'QPR'])
    plt.ylim(ymin=0)
    plt.title(f'Speedups over QP3 for XPS 9300 ({threads} threads)')
    plt.show()


def plot_flop_rates(threads):
    data = helpers.read_exp1_data('xps', threads)
    qrf, qp3, qpr = helpers.exp1_times_means_and_stddevs(data)
    plt.plot(qrf[0], helpers.effective_gflops_square(qrf[0], qrf[1]), c='b')
    plt.plot(qpr[0], helpers.effective_gflops_square(qpr[0], qpr[1]), c='k')
    plt.plot(qp3[0], helpers.effective_gflops_square(qp3[0], qp3[1]), c='r')
    plt.legend(['QRF', 'QPR', 'QP3'])
    plt.ylabel('GFlops')
    plt.ylim(ymin=0)
    plt.xlabel('n')
    plt.title(f'Standardized GFlops for XPS 9300 ({threads} threads)')
    plt.show()
    pass


if __name__ == '__main__':
    plot_speedups(4)
    plot_flop_rates(4)
