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


double time_dgeqrx(int64_t m_A, int64_t n_A, double *buff_A, char x)
{
  int64_t *buff_p   = ( int64_t * ) calloc( n_A, sizeof( int64_t ) );
  double *buff_tau = ( double * ) malloc( n_A * sizeof( double ) );
  auto t1 = high_resolution_clock::now();
  switch (x)
  {
    case '3': 
      lapack::geqp3(m_A, n_A, buff_A, m_A, buff_p, buff_tau);
      break;
    case 'R':
      HQRRP::dgeqpr(m_A, n_A, buff_A, m_A, buff_p, buff_tau);
      break;
    case 'F':
      lapack::geqrf(m_A, n_A, buff_A, m_A, buff_tau);
      break;
    default:
      return -1;
  }
  auto t2 = high_resolution_clock::now();
  double t = (double) duration_cast<milliseconds>(t2 - t1).count();
  free( buff_p );
  free( buff_tau );
  return t;
}


// ============================================================================
int main( int argc, char *argv[] ) {
  using namespace HQRRP;

  int64_t m_A      = 5000;
  int64_t n_A      = 5000;
  double *buff_A   = ( double * ) malloc( m_A * n_A * sizeof( double ) );

  // populate the test matrix and call MKL for unpivoted QR
  genmat(m_A, n_A, buff_A, (uint64_t) 0);
  double tu = time_dgeqrx(m_A, n_A, buff_A, 'F');
  std::cout << tu << "ms for unpivoted QR with LAPACK++\n";

  // **RE**populate the test matrix and run the randomized algorithm.
  genmat(m_A, n_A, buff_A, (uint64_t) 0);
  double t4 = time_dgeqrx(m_A, n_A, buff_A, 'R');
  std::cout << t4 << "ms for HQRRP\n";

  // **RE**populate the test matrix and call MKL
  genmat(m_A, n_A, buff_A, (uint64_t) 0);
  double t3 = time_dgeqrx(m_A, n_A, buff_A, '3');
  std::cout << t3 << "ms for pivoted QR (QP3) with LAPACK++\n";

  free( buff_A );
  return 0;
}
