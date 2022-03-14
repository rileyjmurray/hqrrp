configure_file(CMake/hqrrpConfig.cmake.in
    ${CMAKE_INSTALL_LIBDIR}/cmake/hqrrpConfig.cmake @ONLY)

install(FILES
    ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}/cmake/hqrrpConfig.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake)
