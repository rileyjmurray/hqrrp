export VECLIB_MAXIMUM_THREADS=4
./experiment1 > exp1_log_intelmac_4threads.csv
export VECLIB_MAXIMUM_THREADS=2
./experiment1 > exp1_log_intelmac_2threads.csv
