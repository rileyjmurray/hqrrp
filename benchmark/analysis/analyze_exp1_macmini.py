import numpy as np
from matplotlib import pyplot as plt
import analysis.helpers as helpers


def plot_speedups_and_rates():
    data = helpers.read_exp1_data('macmini', '')

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

    fig.suptitle(f'M1 Mac Mini: Accelerate', y=0.95, fontsize='large')
    fig.savefig(f'macmini_fig.pdf')
    fig.show()


if __name__ == '__main__':
    plot_speedups_and_rates()
