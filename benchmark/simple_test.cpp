#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <blas.hh>
#include <hqrrp.h>
#include <mkl.h>


#define max( a, b ) ( (a) > (b) ? (a) : (b) )
#define min( a, b ) ( (a) < (b) ? (a) : (b) )

// #define int64_t lapack_int
// ^ Might be needed if LAPACK++ is linked against a library in the LP64 model (as opposed to ILP64)


// ============================================================================
// Declaration of local prototypes.

static void set_pvt_to_zero( int64_t n_p, int64_t * buff_p );



// ============================================================================
int main( int argc, char *argv[] ) {
  using namespace HQRRP;
  
  int64_t     nb_alg, pp, m_A, n_A, mn_A, ldim_A, ldim_Q, info, lwork;
  double  * buff_A, * buff_tau, * buff_Q, * buff_wk_qp4, * buff_wk_orgqr;
  int64_t     * buff_p;

  // Create matrix A, vector p, vector s, and matrix Q.
  m_A      = 300;
  n_A      = 100;
  mn_A     = min( m_A, n_A );
  buff_A   = ( double * ) malloc( m_A * n_A * sizeof( double ) );
  ldim_A   = max( 1, m_A );

  buff_p   = ( int64_t * ) malloc( n_A * sizeof( int64_t ) );

  buff_tau = ( double * ) malloc( n_A * sizeof( double ) );

  buff_Q   = ( double * ) malloc( m_A * mn_A * sizeof( double ) );
  ldim_Q   = max( 1, m_A );

  // Generate matrix.
  genmat(m_A, n_A, buff_A, (uint64_t) 0);

  // Initialize vector with pivots.
  set_pvt_to_zero( n_A, buff_p );
  lwork       = max( 1, 128 * n_A );
  buff_wk_qp4 = ( double * ) malloc( lwork * sizeof( double ) );

  // Factorize matrix.
  printf( "%% Just before computing factorization.\n" );
  // New factorization.
  dgeqp4( & m_A, & n_A, buff_A, & ldim_A, buff_p, buff_tau, 
          buff_wk_qp4, & lwork, & info );
  // Current factorization.
  // dgeqp3_( & m_A, & n_A, buff_A, & ldim_A, buff_p, buff_tau, 
  //          buff_wk_qp4, & lwork, & info );
  printf( "%% Just after computing factorization.\n" );

  printf( "%% Info after factorization:      %d \n", info );
  printf( "%% Work[ 0 ] after factorization: %d \n", ( int64_t ) buff_wk_qp4[ 0 ] );

  // Remove workspace.
  free( buff_wk_qp4 );

  // Free matrices and vectors.
  free( buff_A );
  free( buff_p );
  free( buff_tau );
  free( buff_Q );

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
