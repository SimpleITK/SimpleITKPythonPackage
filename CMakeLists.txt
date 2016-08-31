
cmake_minimum_required(VERSION 3.3)

project(SimpleITKPythonPackage NONE)

if(NOT DEFINED SimpleITKPythonPackage_SUPERBUILD)
  set(SimpleITKPythonPackage_SUPERBUILD 1)
endif()

if(SimpleITKPythonPackage_SUPERBUILD)

  # compile with multiple processors
  include(ProcessorCount)
  ProcessorCount(NPROC)
  if (NOT NPROC EQUAL 0)
    set( ENV{MAKEFLAGS} "-j${NPROC}" )
  endif()

  include(ExternalProject)

  set(SimpleITK_REPOSITORY git://github.com/jcfr/SimpleITK)
  set(SimpleITK_GIT_TAG "simpify-python-packaging") #v0.10.0)

  set(SimpleITK_SOURCE_DIR ${CMAKE_BINARY_DIR}/SimpleITK)

  # A separate project is used to download SimpleITK, so that the SuperBuild
  # subdirectory can be use for SimpleITK's SuperBuild to build the
  # required Lua, GTest etc.
  ExternalProject_add( SimpleITK-download
    SOURCE_DIR ${SimpleITK_SOURCE_DIR}
    GIT_REPOSITORY ${SimpleITK_REPOSITORY}
    GIT_TAG ${SimpleITK_GIT_TAG}
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    )

  set(SimpleITK_SUPERBUILD_DIR ${CMAKE_BINARY_DIR}/SimpleITK-superbuild)

  # The actual SimpleITK Superbuild project that build all the tools
  # needed (GTest, PCRE, Swig, Lua & GTest) and then SimpleITK itself.
  ExternalProject_add(SimpleITK-superbuild
    SOURCE_DIR ${SimpleITK_SOURCE_DIR}/SuperBuild
    BINARY_DIR ${SimpleITK_SUPERBUILD_DIR}
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CMAKE_CACHE_ARGS
      -DBUILD_EXAMPLES:BOOL=OFF
      -DBUILD_TESTING:BOOL=OFF
      -DBUILD_DOXYGEN:BOOL=OFF
      -DWRAP_PYTHON:BOOL=ON
      -DWRAP_TCL:BOOL=OFF
      -DWRAP_JAVA:BOOL=OFF
      -DWRAP_RUBY:BOOL=OFF
      -DWRAP_LUA:BOOL=OFF
      -DWRAP_CSHARP:BOOL=OFF
      -DWRAP_R:BOOL=OFF
      -DSimpleITK_INSTALL_DOC_DIR:STRING=SimpleITK
      -DSimpleITK_BUILD_STRIP:BOOL=ON
      -DSimpleITK_BUILD_DISTRIBUTE:BOOL=ON
    INSTALL_COMMAND ""
    DEPENDS SimpleITK-download
    )

  ExternalProject_add(${PROJECT_NAME}
    SOURCE_DIR ${CMAKE_SOURCE_DIR}
    BINARY_DIR ${CMAKE_BINARY_DIR}/${PROJECT_NAME}-build
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    INSTALL_COMMAND ""
    CMAKE_CACHE_ARGS
      -DSimpleITKPythonPackage_SUPERBUILD:BOOL=0
      -DSimpleITK_DIR:PATH=${SimpleITK_SUPERBUILD_DIR}/SimpleITK-build
      -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
    DEPENDS SimpleITK-superbuild
    )

  install(SCRIPT ${CMAKE_BINARY_DIR}/${PROJECT_NAME}-build/cmake_install.cmake)

else()

  # Install SimpleITK "Runtime" components
  install(CODE "unset(CMAKE_INSTALL_COMPONENT)")
  install(CODE "set(COMPONENT \"Runtime\")")
  install(CODE "include\(\"${SimpleITK_DIR}/cmake_install.cmake\")")

endif()

