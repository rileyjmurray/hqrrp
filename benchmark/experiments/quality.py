import numpy as np
import os
import subprocess
from matplotlib import pyplot as plt


def polynomial_decay(eff_rank, power, n):
    diag = np.ones(n)
    decayer = np.arange(start=2, stop=(n - eff_rank + 2)).astype(float)
    low = decayer ** -power
    diag[eff_rank:] = low
    return diag


def simple(spectrum, seed=0):
    spec_string = str([s for s in spectrum])[1:-1]
    spec_string.replace(',', ' ')
    alg = 'R'
    cwd = os.getcwd()
    command_string = f'{cwd}/../build/./bench_quality {seed} {alg} ' + spec_string
    command_string += ' >> quality_log/simple.csv'
    os.system(command_string)


def run_polydecay_exp1():
    filename = 'polydecay_exp1.csv'
    run_polydecay_generic(500, 1.5, 5000, filename)


def run_polydecay_exp2():
    filename = 'polydecay_exp2.csv'
    run_polydecay_generic(1000, 4, 5000, filename)


def read_polydecay_exp2():
    spectrum = polynomial_decay(1000, 4, 5000)
    data = np.genfromtxt('quality_log/polydecay_exp2.csv', delimiter=',')
    qpr = data[::2, :]
    qp3 = data[1::2, :]
    return spectrum, qpr, qp3


def run_polydecay_generic(eff_rank, p, n, filename):
    spectrum = polynomial_decay(eff_rank, p, n)
    spec_string = str([s for s in spectrum])[1:-1]
    spec_string.replace(',', ' ')
    cwd = os.getcwd()
    base_command_string = f'{cwd}/../build/./bench_quality %s %s ' + spec_string
    trials = 10
    for i in range(trials):
        seed = i*(n**2)
        command_string = base_command_string % (str(seed), 'R')
        command_string += f' >> quality_log/{filename}'
        subprocess.run(command_string, shell=True)
        command_string = base_command_string % (str(seed), 'D')
        command_string += f' >> quality_log/{filename}'
        subprocess.run(command_string, shell=True)
        print(f'Done with step {i + 1} of {trials}')


if __name__ == '__main__':
    s, qpr, qp3 = read_polydecay_exp2()
    scale = 1.5

    """
    h = plt.figure(dpi=400, figsize=(5*scale, 3*scale))
    cx = h.add_subplot()
    cx.semilogy(s, c='b', linewidth=1)
    cx.set_ylabel('sigma[k]', fontsize='medium')
    cx.set_xlabel('k', fontsize='medium')
    cx.grid(alpha=0.25, linestyle='--')
    h.savefig('quality_singvals.pdf')
    h.show()
    """

    f = plt.figure(dpi=400, figsize=(5*scale, 3*scale))
    ax = f.add_subplot()
    for i in range(10):
        ax.semilogy(qpr[i, :], c='k', alpha=0.2, linewidth=1)
        ax.semilogy(qp3[i, :], c='r', alpha=0.2, linewidth=1)
    ax.semilogy(s, color='xkcd:gold', alpha=1.0, linewidth=1)
    ax.set_xlabel('k', fontsize='medium')
    ax.set_ylabel('R[k, k]', fontsize='medium')
    ax.grid(alpha=0.25, linestyle='--')
    f.savefig('quality_diag_r.pdf')
    f.show()

    """
    g = plt.figure(dpi=400, figsize=(5*scale, 3*scale))
    bx = g.add_subplot()
    for i in range(10):
        bx.plot(qpr[i, :] / s, c='k', alpha=0.25, linewidth=1)
        bx.plot(qp3[i, :] / s, c='r', alpha=0.25, linewidth=1)
    bx.set_ylabel('R[k,k] / sigma[k]')
    bx.set_xlabel('k', fontsize='medium')
    bx.grid(alpha=0.25, linestyle='--')
    g.savefig('quality_singval_est_rats.pdf')
    g.show()
    """
