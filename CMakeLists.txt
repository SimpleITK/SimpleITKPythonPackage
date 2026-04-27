
cmake_minimum_required(VERSION 3.26)

project(SimpleITKPythonPackage NONE)

if(DEFINED SimpleITKPythonPackage_SUPERBUILD)
  message(FATAL_ERROR "The SimpleITKPythonPackage_SUPERBUILD is no longer supported. Please refer to the SuperBuild CMakeLists.txt file to build SimpleITK Python packages.") 
endif()

# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  mark_as_advanced(CMAKE_BUILD_TYPE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()

if(NOT DEFINED SimpleITK_SOURCE_DIR)
  set(SimpleITK_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/SimpleITK")
endif()


set(ep_common_cmake_cache_args)
if(NOT CMAKE_CONFIGURATION_TYPES)
  list(APPEND ep_common_cmake_cache_args
    -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
  )
endif()


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

# Find SWIG executable - should be provided by the build environment
find_package ( SWIG )
if ( NOT SWIG_FOUND )
  message(FATAL_ERROR "SWIG executable not found. Please set SWIG_EXECUTABLE variable to point to a valid SWIG executable.")
endif()
message(STATUS "SuperBuild -   Found SWIG_EXECUTABLE: ${SWIG_EXECUTABLE}")
message(STATUS "SuperBuild -   SWIG_VERSION: ${SWIG_VERSION}")

#-----------------------------------------------------------------------------
include(ExternalProject)

#-----------------------------------------------------------------------------

# Sanity checks
if(DEFINED SimpleITK_SOURCE_DIR AND NOT EXISTS ${SimpleITK_SOURCE_DIR})
  message(FATAL_ERROR "SimpleITK_SOURCE_DIR variable is defined but corresponds to nonexistent directory: \"${SimpleITK_SOURCE_DIR}\"")
endif()

message(STATUS "SuperBuild -   SimpleITK_SOURCE_DIR: ${SimpleITK_SOURCE_DIR}")

#-----------------------------------------------------------------------------
# SimpleITK "Core" libraries: This is the SimpleITK Superbuild project
# that build all the tools needed (GTest, PCRE, Swig, Lua & GTest) and
# then SimpleITK "core" libraries.

message(STATUS "SuperBuild - SimpleITK-superbuild")

# Sanity checks
if(DEFINED SimpleITK_DIR AND NOT EXISTS ${SimpleITK_DIR})
  message(FATAL_ERROR "SimpleITK_DIR variable is defined but corresponds to nonexistent directory")
endif()
if(DEFINED SWIG_EXECUTABLE AND NOT EXISTS ${SWIG_EXECUTABLE})
  message(FATAL_ERROR "SWIG_EXECUTABLE variable is defined but corresponds to nonexistent file")
endif()

set( SimpleITK-python-deps "" )

if(NOT DEFINED SimpleITK_DIR)

  set(SimpleITK_SUPERBUILD_DIR ${CMAKE_BINARY_DIR}/sitk-sb)

  ExternalProject_add(SimpleITK-superbuild
    SOURCE_DIR ${SimpleITK_SOURCE_DIR}/SuperBuild
    BINARY_DIR ${SimpleITK_SUPERBUILD_DIR}
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CMAKE_CACHE_ARGS
      ${ep_common_cmake_cache_args}
      -DBUILD_EXAMPLES:BOOL=OFF
      -DBUILD_TESTING:BOOL=OFF
      -DBUILD_DOXYGEN:BOOL=OFF
      -DWRAP_DEFAULT:BOOL=OFF
      -DITK_USE_BUILD_DIR:BOOL=ON
      -DSimpleITK_INSTALL_DOC_DIR:STRING=SimpleITK
      -DSimpleITK_BUILD_STRIP:BOOL=ON
      -DSimpleITK_BUILD_DISTRIBUTE:BOOL=ON
      -DSimpleITK_GIT_PROTOCOL:STRING=https
      -DSimpleITK_USE_SYSTEM_SWIG:BOOL=ON
      -DSWIG_EXECUTABLE:PATH=${SWIG_EXECUTABLE}
      -DSKBUILD:BOOL=${SKBUILD}
      -DUSE_CCACHE:BOOL=${USE_CCACHE}
    USES_TERMINAL_CONFIGURE 1
    USES_TERMINAL_BUILD 1
    INSTALL_COMMAND ""
    )

  set(SimpleITK_DIR ${SimpleITK_SUPERBUILD_DIR}/SimpleITK-build)
  set(ITK_DIR  ${SimpleITK_SUPERBUILD_DIR}/ITK-build)
  list(APPEND SimpleITK-python-deps SimpleITK-superbuild)

endif()

message(STATUS "SuperBuild -   SimpleITK_DIR: ${SimpleITK_DIR}")
message(STATUS "SuperBuild -   ITK_DIR: ${ITK_DIR}")
message(STATUS "SuperBuild -   SWIG_EXECUTABLE: ${SWIG_EXECUTABLE}")


#-----------------------------------------------------------------------------
if(NOT SimpleITKPythonPackage_BUILD_PYTHON)
  return()
endif()


#-----------------------------------------------------------------------------
# Search for python interpreter and libraries

message(STATUS "SuperBuild - Searching for python")

if ( PYTHON_VERSION_STRING VERSION_GREATER_EQUAL "3.11.0")

  set(_SimpleITK_PYTHON_USE_LIMITED_API_DEFAULT ON)
else ()
  set(_SimpleITK_PYTHON_USE_LIMITED_API_DEFAULT OFF)
endif()
option( SimpleITK_PYTHON_USE_LIMITED_API "Use Python limited API, for minor version compatibility." ${_SimpleITK_PYTHON_USE_LIMITED_API_DEFAULT} )

# Sanity checks
if(DEFINED Python_INCLUDE_DIR AND NOT EXISTS ${Python_INCLUDE_DIR})
  message(FATAL_ERROR "Python_INCLUDE_DIR variable is defined but corresponds to nonexistent directory")
endif()
if(DEFINED Python_LIBRARY AND NOT EXISTS ${Python_LIBRARY})
  message(FATAL_ERROR "Python_LIBRARY variable is defined but corresponds to nonexistent file")
endif()
if(DEFINED Python_EXECUTABLE AND NOT EXISTS ${Python_EXECUTABLE})
  message(FATAL_ERROR "Python_EXECUTABLE variable is defined but corresponds to nonexistent file")
endif()

if(NOT DEFINED Python_INCLUDE_DIR
    OR NOT DEFINED Python_LIBRARY
    OR NOT DEFINED Python_EXECUTABLE)

  find_package( Python COMPONENTS Interpreter Development REQUIRED )

endif()

message(STATUS "SuperBuild -   Python_INCLUDE_DIR: ${Python_INCLUDE_DIR}")
message(STATUS "SuperBuild -   Python_LIBRARY: ${Python_LIBRARY}")
message(STATUS "SuperBuild -   Python_EXECUTABLE: ${Python_EXECUTABLE}")


#-----------------------------------------------------------------------------
# SimpleITK Python module: This project build only the SimpleITK python
# module.

message(STATUS "SuperBuild - SimpleITK-python => Requires ${SimpleITK-python-deps}")
message(STATUS "SuperBuild -   INSTALL_DIR: ${SKBUILD_SCRIPTS_DIR}")
set(SimpleITK_PYTHON_DIR "${CMAKE_BINARY_DIR}/SimpleITK-python")

ExternalProject_add(SimpleITK-python
  SOURCE_DIR ${SimpleITK_SOURCE_DIR}/Wrapping/Python
  BINARY_DIR ${SimpleITK_PYTHON_DIR}
  DOWNLOAD_COMMAND ""
  UPDATE_COMMAND ""
  INSTALL_COMMAND ""
  CMAKE_CACHE_ARGS
    ${ep_common_cmake_cache_args}
    -DPython_INCLUDE_DIR:PATH=${Python_INCLUDE_DIR}
    -DPython_LIBRARY:PATH=${Python_LIBRARY}
    -DPython_EXECUTABLE:PATH=${Python_EXECUTABLE}
    -DBUILD_TESTING:BOOL=OFF
    -DSimpleITK_PYTHON_THREADS:BOOL=${SimpleITK_PYTHON_THREADS}
    -DSimpleITK_PYTHON_USE_LIMITED_API:BOOL=${SimpleITK_PYTHON_USE_LIMITED_API}
    -DSimpleITK_DIR:PATH=${SimpleITK_DIR}
    -DITK_DIR:PATH=${ITK_DIR}
    -DSWIG_EXECUTABLE:PATH=${SWIG_EXECUTABLE}
    -DSimpleITK_BUILD_STRIP:BOOL=ON
    -DSKBUILD:BOOL=ON
    -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
  USES_TERMINAL_CONFIGURE 1
  USES_TERMINAL_BUILD 1

  DEPENDS "${SimpleITK-python-deps}"
  )


#-----------------------------------------------------------------------------
# Install SimpleITK Python "Runtime" components
install(CODE "
unset(CMAKE_INSTALL_COMPONENT)
set(COMPONENT \"Runtime\")
include\(\"${SimpleITK_PYTHON_DIR}/cmake_install.cmake\")
unset(CMAKE_INSTALL_COMPONENT)
")

