import numpy as np
import os
import subprocess


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


def polydecay_exp1():
    n = 5000
    spectrum = polynomial_decay(500, 1.5, n)
    spec_string = str([s for s in spectrum])[1:-1]
    spec_string.replace(',', ' ')
    cwd = os.getcwd()
    base_command_string = f'{cwd}/../build/./bench_quality %s %s ' + spec_string
    trials = 10
    for i in range(trials):
        seed = i*(n**2)
        command_string = base_command_string % (str(seed), 'R')
        command_string += ' >> quality_log/polydecay_exp1.csv'
        subprocess.run(command_string, shell=True)
        command_string = base_command_string % (str(seed), 'D')
        command_string += ' >> quality_log/polydecay_exp1.csv'
        subprocess.run(command_string, shell=True)
        print(f'Done with step {i + 1} of {trials}')


if __name__ == '__main__':
    polydecay_exp1()
