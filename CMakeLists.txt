
cmake_minimum_required(VERSION 3.3)

project(SimpleITKPythonPackage NONE)

if(NOT DEFINED SimpleITKPythonPackage_SUPERBUILD)
  set(SimpleITKPythonPackage_SUPERBUILD 1)
endif()

if(SimpleITKPythonPackage_SUPERBUILD)

  #-----------------------------------------------------------------------------
  # Options
  option ( SimpleITK_PYTHON_THREADS "Enable threaded python usage by unlocking the GIL." ON )
  mark_as_advanced( SimpleITK_PYTHON_THREADS )

  #
  # When building different "flavor" of SimpleITK python packages on a given platform,
  # explicitly setting the following options allow to speed up package generation by
  # re-using existing resources.
  #
  #  SimpleITK_SOURCE_DIR: Path to an existing source directory
  #
  #  SWIG_EXECUTABLE: Path to an existing executable
  #
  #  SimpleITK_DIR: Path to an existing SimpleITK build or install directory
  #

  option ( SimpleITKPythonPackage_BUILD_PYTHON "Build SimpleITK python module" ON )
  mark_as_advanced( SimpleITKPythonPackage_BUILD_PYTHON )

  # compile with multiple processors
  include(ProcessorCount)
  ProcessorCount(NPROC)
  if (NOT NPROC EQUAL 0)
    set( ENV{MAKEFLAGS} "-j${NPROC}" )
  endif()

  #-----------------------------------------------------------------------------
  include(ExternalProject)

  set(SimpleITK_REPOSITORY https://itk.org/SimpleITK.git)
  set(SimpleITK_GIT_TAG "4302e2b12ba8507f680b32deb23e4b25d2616003") #1.0.0.dev19

  # Add an empty external project
  function(sitk_ExternalProject_Add_Empty proj depends)
    set(depends_args)
    if(NOT depends STREQUAL "")
      set(depends_args DEPENDS ${depends})
    endif()
    ExternalProject_add(${proj}
      SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj}
      DOWNLOAD_COMMAND ""
      UPDATE_COMMAND ""
      CONFIGURE_COMMAND ""
      BUILD_COMMAND ""
      BUILD_IN_SOURCE 1
      BUILD_ALWAYS 1
      INSTALL_COMMAND ""
      ${depends_args}
      )
  endfunction()


  #-----------------------------------------------------------------------------
  # A separate project is used to download SimpleITK, so that the SuperBuild
  # subdirectory can be use for SimpleITK's SuperBuild to build the
  # required Lua, GTest etc.

  message(STATUS "SuperBuild - SimpleITK-download")

  # Sanity checks
  if(DEFINED SimpleITK_SOURCE_DIR AND NOT EXISTS ${SimpleITK_SOURCE_DIR})
    message(FATAL_ERROR "SimpleITK_SOURCE_DIR variable is defined but corresponds to nonexistent directory")
  endif()

  if(NOT DEFINED SimpleITK_SOURCE_DIR)

    set(SimpleITK_SOURCE_DIR ${CMAKE_BINARY_DIR}/SimpleITK)

    ExternalProject_add(SimpleITK-download
      SOURCE_DIR ${SimpleITK_SOURCE_DIR}
      GIT_REPOSITORY ${SimpleITK_REPOSITORY}
      GIT_TAG ${SimpleITK_GIT_TAG}
      USES_TERMINAL_DOWNLOAD 1
      CONFIGURE_COMMAND ""
      BUILD_COMMAND ""
      INSTALL_COMMAND ""
      )

  else()

    sitk_ExternalProject_Add_Empty(
      SimpleITK-download
      ""
      )

  endif()

  message(STATUS "SuperBuild -   SimpleITK_SOURCE_DIR: ${SimpleITK_SOURCE_DIR}")

  #-----------------------------------------------------------------------------
  # SimpleITK "Core" libraries: This is the SimpleITK Superbuild project
  # that build all the tools needed (GTest, PCRE, Swig, Lua & GTest) and
  # then SimpleITK "core" libraries.

  message(STATUS "SuperBuild - SimpleITK-superbuild => Requires SimpleITK-download")

  # Sanity checks
  if(DEFINED SimpleITK_DIR AND NOT EXISTS ${SimpleITK_DIR})
    message(FATAL_ERROR "SimpleITK_DIR variable is defined but corresponds to nonexistent directory")
  endif()
  if(DEFINED SWIG_EXECUTABLE AND NOT EXISTS ${SWIG_EXECUTABLE})
    message(FATAL_ERROR "SWIG_EXECUTABLE variable is defined but corresponds to nonexistent file")
  endif()

  if(NOT DEFINED SimpleITK_DIR AND NOT DEFINED SWIG_EXECUTABLE)

    set(SimpleITK_SUPERBUILD_DIR ${CMAKE_BINARY_DIR}/SimpleITK-superbuild)

    ExternalProject_add(SimpleITK-superbuild
      SOURCE_DIR ${SimpleITK_SOURCE_DIR}/SuperBuild
      BINARY_DIR ${SimpleITK_SUPERBUILD_DIR}
      DOWNLOAD_COMMAND ""
      UPDATE_COMMAND ""
      CMAKE_CACHE_ARGS
        -DBUILD_EXAMPLES:BOOL=OFF
        -DBUILD_TESTING:BOOL=OFF
        -DBUILD_DOXYGEN:BOOL=OFF
        -DWRAP_PYTHON:BOOL=OFF
        -DWRAP_TCL:BOOL=OFF
        -DWRAP_JAVA:BOOL=OFF
        -DWRAP_RUBY:BOOL=OFF
        -DWRAP_LUA:BOOL=OFF
        -DWRAP_CSHARP:BOOL=OFF
        -DWRAP_R:BOOL=OFF
        -DSimpleITK_INSTALL_DOC_DIR:STRING=SimpleITK
        -DSimpleITK_BUILD_STRIP:BOOL=ON
        -DSimpleITK_BUILD_DISTRIBUTE:BOOL=ON
        -DSITK_GIT_PROTOCOL:STRING=git
        -DSKBUILD:BOOL=${SKBUILD}
      USES_TERMINAL_CONFIGURE 1
      USES_TERMINAL_BUILD 1
      INSTALL_COMMAND ""
      DEPENDS SimpleITK-download
      )

    ExternalProject_Add_StepDependencies(SimpleITK-superbuild download SimpleITK-download)

    set(SimpleITK_DIR ${SimpleITK_SUPERBUILD_DIR}/SimpleITK-build)
    if(WIN32)
      set(SWIG_TARGET_VERSION "3.0.10")
      set(SWIG_EXECUTABLE ${SimpleITK_SUPERBUILD_DIR}/swigwin-${SWIG_TARGET_VERSION}/swig.exe)
    else()
      set(SWIG_EXECUTABLE ${SimpleITK_SUPERBUILD_DIR}/Swig/bin/swig)
    endif()
  else()

    sitk_ExternalProject_Add_Empty(
      SimpleITK-superbuild
      SimpleITK-download
      )

  endif()

  message(STATUS "SuperBuild -   SimpleITK_DIR: ${SimpleITK_DIR}")
  message(STATUS "SuperBuild -   SWIG_EXECUTABLE: ${SWIG_EXECUTABLE}")


  #-----------------------------------------------------------------------------
  if(NOT SimpleITKPythonPackage_BUILD_PYTHON)
    return()
  endif()


  #-----------------------------------------------------------------------------
  # Search for python interpreter and libraries

  message(STATUS "SuperBuild - Searching for python")

  # Sanity checks
  if(DEFINED PYTHON_INCLUDE_DIR AND NOT EXISTS ${PYTHON_INCLUDE_DIR})
    message(FATAL_ERROR "PYTHON_INCLUDE_DIR variable is defined but corresponds to nonexistent directory")
  endif()
  if(DEFINED PYTHON_LIBRARY AND NOT EXISTS ${PYTHON_LIBRARY})
    message(FATAL_ERROR "PYTHON_LIBRARY variable is defined but corresponds to nonexistent file")
  endif()
  if(DEFINED PYTHON_EXECUTABLE AND NOT EXISTS ${PYTHON_EXECUTABLE})
    message(FATAL_ERROR "PYTHON_EXECUTABLE variable is defined but corresponds to nonexistent file")
  endif()

  if(NOT DEFINED PYTHON_INCLUDE_DIR
     OR NOT DEFINED PYTHON_LIBRARY
     OR NOT DEFINED PYTHON_EXECUTABLE)

    find_package ( PythonLibs REQUIRED )
    find_package ( PythonInterp REQUIRED )

  endif()

  message(STATUS "SuperBuild -   PYTHON_INCLUDE_DIR: ${PYTHON_INCLUDE_DIR}")
  message(STATUS "SuperBuild -   PYTHON_LIBRARY: ${PYTHON_LIBRARY}")
  message(STATUS "SuperBuild -   PYTHON_EXECUTABLE: ${PYTHON_EXECUTABLE}")


  #-----------------------------------------------------------------------------
  # SimpleITK Python module: This project build only the SimpleITK python
  # module.

  message(STATUS "SuperBuild - SimpleITK-python => Requires SimpleITK-superbuild")

  set(SimpleITK_PYTHON_DIR "${CMAKE_BINARY_DIR}/SimpleITK-python")

  ExternalProject_add(SimpleITK-python
    SOURCE_DIR ${SimpleITK_SOURCE_DIR}/Wrapping/Python
    BINARY_DIR ${SimpleITK_PYTHON_DIR}
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CMAKE_CACHE_ARGS
      -DPYTHON_INCLUDE_DIR:PATH=${PYTHON_INCLUDE_DIR}
      -DPYTHON_LIBRARY:PATH=${PYTHON_LIBRARY}
      -DPYTHON_EXECUTABLE:PATH=${PYTHON_EXECUTABLE}
      -DSimpleITK_PYTHON_THREADS:BOOL=${SimpleITK_PYTHON_THREADS}
      -DSimpleITK_DIR:PATH=${SimpleITK_DIR}
      -DSWIG_EXECUTABLE:PATH=${SWIG_EXECUTABLE}
      -DSimpleITK_BUILD_STRIP:BOOL=ON
      -DSKBUILD:BOOL=ON
    USES_TERMINAL_CONFIGURE 1
    USES_TERMINAL_BUILD 1
    INSTALL_COMMAND ""
    DEPENDS SimpleITK-superbuild
    )

  message(STATUS "SuperBuild -   SimpleITK_PYTHON_DIR: ${SimpleITK_PYTHON_DIR}")

  ExternalProject_Add_StepDependencies(SimpleITK-python download SimpleITK-download)


  #-----------------------------------------------------------------------------
  # SimpleITKPythonPackage: This project adds install rules for the "Runtime" component
  # of both SimpleITK code and python libraries.

  message(STATUS "SuperBuild - ${PROJECT_NAME} => Requires SimpleITK-python")

  ExternalProject_add(${PROJECT_NAME}
    SOURCE_DIR ${CMAKE_SOURCE_DIR}
    BINARY_DIR ${CMAKE_BINARY_DIR}/${PROJECT_NAME}-build
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CMAKE_CACHE_ARGS
      -DSimpleITKPythonPackage_SUPERBUILD:BOOL=0
      -DSimpleITK_DIR:PATH=${SimpleITK_DIR}
      -DSimpleITK_PYTHON_DIR:PATH=${SimpleITK_PYTHON_DIR}
      -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
    USES_TERMINAL_CONFIGURE 1
    INSTALL_COMMAND ""
    DEPENDS SimpleITK-python
    )

  install(SCRIPT ${CMAKE_BINARY_DIR}/${PROJECT_NAME}-build/cmake_install.cmake)

else()

  #-----------------------------------------------------------------------------
  # Install SimpleITK Core "Runtime" components
  install(CODE "
unset(CMAKE_INSTALL_COMPONENT)
set(COMPONENT \"Runtime\")
include\(\"${SimpleITK_DIR}/cmake_install.cmake\")
unset(CMAKE_INSTALL_COMPONENT)
")

  # Install SimpleITK Python "Runtime" components
  install(CODE "
unset(CMAKE_INSTALL_COMPONENT)
set(COMPONENT \"Runtime\")
include\(\"${SimpleITK_PYTHON_DIR}/cmake_install.cmake\")
unset(CMAKE_INSTALL_COMPONENT)
")

endif()

