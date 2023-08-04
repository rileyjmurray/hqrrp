set(
    hqrrp_cxx
    ${PROJECT_SOURCE_DIR}/src/hqrrp.cpp
    ${PROJECT_SOURCE_DIR}/src/util.cpp
)
add_library(
    hqrrp ${hqrrp_cxx}
)
set(
  hqrrp_cxx_opts
  -Wall -Wextra
)
if (SANITIZE_ADDRESS)
    list(APPEND hqrrp_cxx_opts -fsanitize=address)
    target_link_options(hqrrp INTERFACE -fsanitize=address)
endif()

target_include_directories(
    hqrrp PUBLIC
    $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${Random123_DIR}>
    $<INSTALL_INTERFACE:include>
)

target_compile_options(
  hqrrp PUBLIC ${hqrrp_cxx_opts}
)

target_link_libraries(hqrrp PUBLIC blaspp lapackpp)

install(DIRECTORY "${CMAKE_SOURCE_DIR}/include/"
  DESTINATION include FILES_MATCHING PATTERN "*.h")

install(TARGETS hqrrp EXPORT hqrrp
  INCLUDES DESTINATION include ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(EXPORT hqrrp DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake
  EXPORT_LINK_INTERFACE_LIBRARIES)
