message(STATUS "Checking for blaspp ... ")
find_package(blaspp REQUIRED)
message(STATUS "Checking for blaspp ... ${blaspp_VERSION}")

add_library(hqrrp_blaspp INTERFACE)

target_link_libraries(hqrrp_blaspp INTERFACE blaspp)

install(TARGETS hqrrp_blaspp EXPORT hqrrp_blaspp)

install(EXPORT hqrrp_blaspp
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake"
    EXPORT_LINK_INTERFACE_LIBRARIES    
)