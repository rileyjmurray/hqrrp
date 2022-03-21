cmake_minimum_required(VERSION 3.10)

project(benchmark)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

message(STATUS "Checking for hqrrp ... ")
find_package(hqrrp REQUIRED)
message(STATUS "Done checking for hqrrp. ...")

message(STATUS "Looking for BLAS++ ... ")
find_package(blaspp REQUIRED)
message(STATUS "Done looking for BLAS++.")

message(STATUS "Looking for LAPACK++ ...")
find_package(lapackpp REQUIRED)
message(STATUS "Done looking for LAPACK++.")

message(STATUS "Looking for MKL ...")
find_package(MKL CONFIG)
message(STATUS "${MKL_IMPORTED_TARGETS}") 
message(STATUS "Done looking for MKL.")

set(
    bench_mklvhqrrp_cxx
    bench_mklvhqrrp.cpp
)
add_executable(
    bench_mklvhqrrp ${bench_mklvhqrrp_cxx}
)
target_include_directories(
    bench_mklvhqrrp PUBLIC ${Random123_DIR} ${MKL_INCLUDE}
)
target_link_libraries(
     bench_mklvhqrrp PUBLIC hqrrp blaspp lapackpp ${MKL}
)


set(
    bench_blocksizes_cxx
    bench_blocksizes.cpp
)
add_executable(
    bench_blocksizes ${bench_blocksizes_cxx}
)
target_include_directories(
    bench_blocksizes PUBLIC ${Random123_DIR} ${MKL_INCLUDE}
)
target_link_libraries(
    bench_blocksizes PUBLIC hqrrp blaspp lapackpp ${MKL}
)


set(
    experiment1_cxx
    experiment1.cpp
)
add_executable(
    experiment1 ${experiment1_cxx}
)
target_include_directories(
    experiment1 PUBLIC ${Random123_DIR} ${MKL_INCLUDE}
)
target_link_libraries(
    experiment1 PUBLIC hqrrp blaspp lapackpp ${MKL}
)



# cmake -DCMAKE_BINARY_DIR=`pwd` -Dhqrrp_DIR=`pwd`/../../hqrrp-install/lib/cmake -DMKL_DIR=/home/riley/intel/oneapi/mkl/latest/lib/cmake/mkl -DMKL_THREADING=gnu_thread -DRandom123_DIR=/opt/random123/include ..
