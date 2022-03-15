message(STATUS "Checking for lapackpp ... ")
find_package(lapackpp REQUIRED)
message(STATUS "Checking for lapackpp ... ${lapackpp_VERSION}")

add_library(hqrrp_lapackpp INTERFACE)

target_link_libraries(hqrrp_lapackpp INTERFACE lapackpp)

install(TARGETS hqrrp_lapackpp EXPORT hqrrp_lapackpp)

install(EXPORT hqrrp_lapackpp
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake"
    EXPORT_LINK_INTERFACE_LIBRARIES    
)