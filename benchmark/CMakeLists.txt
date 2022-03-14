cmake_minimum_required(VERSION 3.10)

project(simple_test)

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

set(
    simple_test_cxx
    simple_test.cpp
)
add_executable(
    simple_test ${simple_test_cxx}
)
target_include_directories(
    simple_test PUBLIC ${Random123_DIR}
)
target_link_libraries(
    simple_test PUBLIC hqrrp blaspp lapackpp
)

