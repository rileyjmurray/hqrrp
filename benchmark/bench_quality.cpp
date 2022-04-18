#include <blas.hh>
#include <hqrrp.h>

#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <chrono>
#include <assert.h>

#define max( a, b ) ( (a) > (b) ? (a) : (b) )
#define min( a, b ) ( (a) < (b) ? (a) : (b) )


using std::chrono::high_resolution_clock;
using std::chrono::duration_cast;
using std::chrono::duration;
using std::chrono::milliseconds;


void haar_matrix(
        double *buff_Q,
        int64_t m,
        int64_t n,
        uint64_t seed)
{   
    assert(m >= n);
    HQRRP::genmat_normal(m, n, buff_Q, seed);
    double *buff_tau = ( double * ) malloc( n * sizeof( double ) );
    lapack::geqrf(m, n, buff_Q, m, buff_tau);
    lapack::orgqr(m, n, n, buff_Q, m, buff_tau);
    free(buff_tau);
}

/*
Need:
  Quality metrics:
    Vector of operator norms of trailing submatrices
    Diagonal entries of R.
  Reference values:
    singular values of the matrix
  Main testing method:
    Read file where the first line is the vector of singular values
    Generates a bunch of SQUARE matrices where the singular vectors are haar distributed.
    Run QP3 and QPR on each matrix.
    For each matrix, record the diagonal entries of R.
    File format:
      singvals ....
      [seed] [alg] diag(R)
      [seed] [alg] trailing submatrix norms.
*/



// ============================================================================
int main( int argc, char *argv[] ) {
  using namespace HQRRP;

  assert(argc >= 4);
  uint64_t seed = strtoul(argv[1], nullptr, 0);
  char alg = *argv[2];

  // singular values
  int64_t m = (int64_t) (argc - 3);
  double *singvals = ( double * ) malloc( m * sizeof( double ));
  for (int i = 3; i <= m + 1; ++i) 
  {
    singvals[i - 3] = atof(argv[i]);
  }
  singvals[m - 1] = atof(argv[m + 2]);

  // Scaled left singular vectors
  double *U = ( double * ) malloc( m * m * sizeof( double ));
  haar_matrix(U, m, m, seed + m*m);
  for (int i = 0; i < m; ++i)
  {
    blas::scal(m, singvals[i], &U[i*m], 1);
  }

  // Transposed right singular vectors
  double *V = ( double * ) malloc( m * m * sizeof( double ));
  haar_matrix(V, m, m, seed); // no need for a transpose

  double *A   = ( double * ) malloc( m * m * sizeof( double ) );
  blas::gemm(blas::Layout::ColMajor, blas::Op::NoTrans, blas::Op::NoTrans,
             m, m, m, 1.0, U, m, V, m, 0.0, A, m);

  // Call the QRCP algorithm
  int64_t *buff_p   = ( int64_t * ) calloc( m, sizeof( int64_t ) );
  double *buff_tau = ( double * ) malloc( m * sizeof( double ) );
  if (alg == 'R')
  {
  // std::cout << "Hit QPR path" << std::endl;
    dgeqpr(m, m, A, m, buff_p, buff_tau);
  }
  else 
  {
    // std::cout << "Hit QP3 path" << std::endl;
    lapack::geqp3(m, m, A, m, buff_p, buff_tau);
  }

  // print the results
  for (int i = 0; i < m - 1; ++i)
  {
    std::cout << abs(A[i + m*i]) << ", ";
  }
  std::cout << abs(A[m*m - 1]);
  std::cout << std::endl;

  free( A );
  free( U );
  free( V );
  free( singvals );
  free( buff_p );
  free( buff_tau );
  return 0;
}
