#include <blas.hh>
#include <hqrrp.h>
#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <bits/stdc++.h>


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
    case '4':
      HQRRP::dgeqp4(m_A, n_A, buff_A, m_A, buff_p, buff_tau);
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

  for (int64_t m_A : {1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000})
  {
    int64_t n_A = m_A;
    double *buff_A   = ( double * ) malloc( m_A * n_A * sizeof( double ) );
    for (char test_dist : {'u', 'n'})
    {
        for (uint64_t test_seed : {0, 1, 2, 3, 4, 5, 6, 7, 8, 9})
        {
            std::string line_prefix = std::to_string(m_A) + ", " + std::to_string(n_A)
                + ", " + std::string(1, test_dist) + ", " + std::to_string(test_seed);

            // warm up the processor
            HQRRP::genmat(1000, 1000, buff_A, 0, 'u');
            time_dgeqrx(1000, 1000, buff_A, '3');

            // populate the test matrix and call MKL for unpivoted QR
            HQRRP::genmat(m_A, n_A, buff_A, test_seed, test_dist);
            double tu = time_dgeqrx(m_A, n_A, buff_A, 'F');
            std::cout << line_prefix << ", QRF, " << tu << std::endl;

            // **RE**populate the test matrix and run the randomized algorithm.
            HQRRP::genmat(m_A, n_A, buff_A, test_seed, test_dist);
            double t4 = time_dgeqrx(m_A, n_A, buff_A, '4');
            std::cout << line_prefix << ", QP4, " << t4 << std::endl;

            // **RE**populate the test matrix and call MKL
            HQRRP::genmat(m_A, n_A, buff_A, test_seed, test_dist);
            double t3 = time_dgeqrx(m_A, n_A, buff_A, '3');
            std::cout << line_prefix << ", QP3, " << t3 << std::endl;
        }
    }
    free(buff_A);
  }
  return 0;
}
