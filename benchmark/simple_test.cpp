#include <blas.hh>
#include <hqrrp.h>
#include <mkl.h>

#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <bits/stdc++.h>

#define max( a, b ) ( (a) > (b) ? (a) : (b) )
#define min( a, b ) ( (a) < (b) ? (a) : (b) )

// #define int64_t lapack_int
// ^ Might be needed if LAPACK++ is linked against a library in the LP64 model (as opposed to ILP64)


using std::chrono::high_resolution_clock;
using std::chrono::duration_cast;
using std::chrono::duration;
using std::chrono::milliseconds;
auto t1 = high_resolution_clock::now();
auto t2 = high_resolution_clock::now();
auto t3 = duration_cast<milliseconds>(t2 - t1);

// ============================================================================
// Declaration of local prototypes.

static void set_pvt_to_zero( int64_t n_p, int64_t * buff_p );



// ============================================================================
int main( int argc, char *argv[] ) {
  using namespace HQRRP;
  
  int64_t     nb_alg, pp, m_A, n_A, ldim_A;
  double  * buff_A, * buff_tau;
  int64_t     * buff_p;

  // Create matrix A, vector p, vector s, and matrix Q.
  m_A      = 5000;
  n_A      = 5000;
  buff_A   = ( double * ) malloc( m_A * n_A * sizeof( double ) );
  ldim_A   = max( 1, m_A );
  buff_p   = ( int64_t * ) malloc( n_A * sizeof( int64_t ) );
  buff_tau = ( double * ) malloc( n_A * sizeof( double ) );


  // Populate the test matrix and run the randomized algorithm.
  genmat(m_A, n_A, buff_A, (uint64_t) 0);
  set_pvt_to_zero( n_A, buff_p );
  t1 = high_resolution_clock::now();
  dgeqp4(m_A, n_A, buff_A, ldim_A, buff_p, buff_tau);
  t2 = high_resolution_clock::now();
  std::cout << duration_cast<milliseconds>(t2 - t1).count() << "ms for HQRRP\n";

  // **RE**populate the test matrix and call MKL
  genmat(m_A, n_A, buff_A, (uint64_t) 0);
  set_pvt_to_zero(n_A, buff_p);
  blas::scal(n_A, 0.0, buff_tau, 1);
  t1 = high_resolution_clock::now();
  lapack::geqp3(m_A, n_A, buff_A, ldim_A, buff_p, buff_tau);
  t2 = high_resolution_clock::now();
  std::cout << duration_cast<milliseconds>(t2 - t1).count() << "ms for MKL\n";

  // Free matrices and vectors.
  free( buff_A );
  free( buff_p );
  free( buff_tau );
  printf( "%% End of Program\n" );

  return 0;
}


// ============================================================================
static void set_pvt_to_zero( int64_t n_p, int64_t * buff_p ) {
  int64_t  i;

  for( i = 0; i < n_p; i++ ) {
    buff_p[ i ] = 0;
  }
}
