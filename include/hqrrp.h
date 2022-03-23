#ifndef LAPACK_HH
#include <lapack.hh>
#include <lapack/config.h>
#define LAPACK_HH
#endif

#ifndef HQRRP_HH
#include <util.h>
#define HQRRP_HH

namespace HQRRP {

void dgeqpr(lapack_int m, lapack_int n, double *A, lapack_int lda, lapack_int *jpvt, double *tau);

void dgeqpr( lapack_int * m, lapack_int * n, double * A, lapack_int * lda, lapack_int * jpvt, double * tau,
         double * work, lapack_int * lwork, lapack_int * info );

lapack_int hqrrp( lapack_int m_A, lapack_int n_A, double * buff_A, lapack_int ldim_A,
        lapack_int * buff_jpvt, double * buff_tau,
        lapack_int nb_alg, lapack_int pp, lapack_int panel_pivoting );

} // end namespace HQRRP

#endif
