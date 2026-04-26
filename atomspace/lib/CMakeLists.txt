# Empty lib directory for build compatibility
INCLUDE(CMakePackageConfigHelpers)

CONFIGURE_PACKAGE_CONFIG_FILE(
    AtomSpaceConfig.cmake.in
    ${CMAKE_BINARY_DIR}/AtomSpaceConfig.cmake
    INSTALL_DESTINATION lib/cmake/AtomSpace
    PATH_VARS CMAKE_INSTALL_PREFIX
)

WRITE_BASIC_PACKAGE_VERSION_FILE(
    "${CMAKE_BINARY_DIR}/AtomSpaceConfigVersion.cmake"
    VERSION ${SEMANTIC_VERSION}
    COMPATIBILITY SameMajorVersion
)

INSTALL(FILES
    ${CMAKE_BINARY_DIR}/AtomSpaceConfig.cmake
    ${CMAKE_BINARY_DIR}/AtomSpaceConfigVersion.cmake
    DESTINATION lib/cmake/AtomSpace)

INSTALL(EXPORT AtomSpaceTargets
    FILE AtomSpaceTargets.cmake
    DESTINATION lib/cmake/AtomSpace)
