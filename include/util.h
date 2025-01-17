#ifndef BLAS_HH
#include <blas.hh>
#define BLAS_HH
#endif


#ifndef HQRRP_UTIL_HH
#define HQRRP_UTIL_HH

namespace HQRRP {

void genmat(int64_t n_rows, int64_t n_cols, double* mat, uint64_t seed);  // uniform [-1, 1]

void genmat(int64_t n_rows, int64_t n_cols, double* mat, uint64_t seed, char dist); // uniform or normal

void genmat_normal(int64_t n_rows, int64_t n_cols, double* mat, uint64_t seed); // normal

void print_double_matrix(
                char * name, int64_t m_A, int64_t n_A, 
                double * buff_A, int64_t ldim_A );

void print_double_vector( char * name, int64_t n_v, double * buff_v );

void print_int_vector( char * name, int64_t n_v, int64_t * buff_v );


} // end namespace HQRRP

#endif  // define HQRRP_UTIL_HH
