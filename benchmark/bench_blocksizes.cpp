#include <blas.hh>
#include <hqrrp.h>

#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <chrono>

#define max( a, b ) ( (a) > (b) ? (a) : (b) )
#define min( a, b ) ( (a) < (b) ? (a) : (b) )


using std::chrono::high_resolution_clock;
using std::chrono::duration_cast;
using std::chrono::duration;
using std::chrono::milliseconds;


double time_hqrrp(int64_t m_A, int64_t n_A, double *buff_A, int64_t nb_alg, bool inner_pivot)
{
  int64_t *buff_p   = ( int64_t * ) calloc( n_A, sizeof( int64_t ) );
  double *buff_tau = ( double * ) malloc( n_A * sizeof( double ) );
  auto t1 = high_resolution_clock::now();
  int64_t ipiv = inner_pivot ? 1 : 0;
  HQRRP::hqrrp(m_A, n_A, buff_A, m_A, buff_p, buff_tau, nb_alg, 10, ipiv);
  auto t2 = high_resolution_clock::now();
  double t = (double) duration_cast<milliseconds>(t2 - t1).count();
  free( buff_p );
  free( buff_tau );
  return t;
}


// ============================================================================
int main( int argc, char *argv[] ) {
  int64_t m_A      = 5000;
  int64_t n_A      = 5000;
  double *buff_A   = ( double * ) malloc( m_A * n_A * sizeof( double ) );

  // populate the test matrix and call MKL for unpivoted QR
  int64_t block_sizes[] = {16, 32, 64, 128};
  for (int64_t nb_alg : block_sizes)
  {
    HQRRP::genmat(m_A, n_A, buff_A, (uint64_t) 0);
    double t = time_hqrrp(m_A, n_A, buff_A, nb_alg, true);
    std::cout << t << "ms for HQRRP with nb_alg = " << nb_alg << " and inner pivoting." << std::endl;
    
    HQRRP::genmat(m_A, n_A, buff_A, (uint64_t) 0);
    t = time_hqrrp(m_A, n_A, buff_A, nb_alg, false);
    std::cout << t << "ms for HQRRP with nb_alg = " << nb_alg << " and NO inner pivoting." << std::endl;
  }


  free( buff_A );
  return 0;
}
