import numpy as np
from matplotlib import pyplot as plt
import analysis.helpers as helpers


def plot_times(threads):
    data = helpers.read_exp1_data('xps', threads)
    qrf, qp3, qpr = helpers.exp1_times_means_and_stddevs(data)
    plt.errorbar(qrf[0], qrf[1]/1000, yerr=qrf[2]/1000, c='b')
    plt.errorbar(qpr[0], qpr[1]/1000, yerr=qpr[2]/1000, c='k')
    plt.errorbar(qp3[0], qp3[1]/1000, yerr=qp3[2]/1000, c='r')
    plt.legend(['QRF', 'QPR', 'QP3'])
    plt.xlabel('n')
    plt.ylabel('seconds')
    plt.title(f'Runtime: XPS 9300, MKL, {threads} threads')
    plt.show()


def plot_speedups(threads):
    data = helpers.read_exp1_data('xps', threads)
    ratf, ratr = helpers.exp1_ratio_means_and_stddevs(data)
    plt.errorbar(ratf[0], ratf[1], yerr=ratf[2], c='b')
    plt.errorbar(ratr[0], ratr[1], yerr=ratr[2], c='k')
    plt.ylim(ymin=0)
    plt.xlabel('n')
    plt.ylabel('(QP3 time) / (alg time)')
    plt.title(f'Speedups over QP3: XPS 9300, MKL, {threads} threads')
    plt.show()


def plot_flop_rates(threads):
    data = helpers.read_exp1_data('xps', threads)
    qrf, qp3, qpr = helpers.exp1_floprates_means_and_stddevs(data)
    plt.errorbar(qrf[0], qrf[1], yerr=qrf[2], c='b')
    plt.errorbar(qpr[0], qpr[1], yerr=qpr[2], c='k')
    plt.errorbar(qp3[0], qp3[1], yerr=qp3[2], c='r')
    plt.legend(['QRF', 'QPR', 'QP3'])
    plt.ylim(ymin=0)
    plt.xlabel('n')
    plt.ylabel('Standardized GFlops')
    plt.title(f'Flop rates: XPS 9300, MKL, {threads} threads')
    plt.show()
    pass


def plot_speedups_and_rates(threads):
    data = helpers.read_exp1_data('xps', threads)

    scale = 1.5
    fig, axs = plt.subplots(2, dpi=400, figsize=(5*scale, 3*scale), sharex=True)

    qrf, qp3, qpr = helpers.exp1_floprates_means_and_stddevs(data)
    axs[1].errorbar(qrf[0], qrf[1], yerr=qrf[2], c='b')
    axs[1].errorbar(qpr[0], qpr[1], yerr=qpr[2], c='k')
    axs[1].errorbar(qp3[0], qp3[1], yerr=qp3[2], c='r')
    axs[1].legend(['QRF', 'QPR', 'QP3'], fontsize='small')
    axs[1].set_ylabel('GFLOPs / sec', fontsize='medium', labelpad=4)
    axs[1].set_ylim(ymin=0)
    axs[1].set_xlabel('n')
    axs[1].grid(alpha=0.25, linestyle='--')
    #axs[1].set_title('Flop rates (standardized)')

    ratf, ratr = helpers.exp1_ratio_means_and_stddevs(data)
    axs[0].errorbar(ratf[0], ratf[1], yerr=ratf[2], c='b')
    axs[0].errorbar(ratr[0], ratr[1], yerr=ratr[2], c='k')
    axs[0].legend(['QRF', 'QPR'], fontsize='small')
    axs[0].set_ylim(ymin=0)
    axs[0].set_ylabel('(QP3 time) / (alg time)', fontsize='medium', labelpad=8)
    axs[0].grid(alpha=0.25, linestyle='--')
    #axs[0].set_title('Speedup relative to classical pivoting (QP3)')

    fig.suptitle('XPS 9300: MKL, 4 threads', y=0.95, fontsize='large')
    fig.savefig('xps_4threads_fig.pdf')
    fig.show()


if __name__ == '__main__':
    #plot_speedups(4)
    #plot_flop_rates(4)
    plot_speedups_and_rates(4)
