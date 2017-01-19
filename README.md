# SimpleITKPythonPackage

This project provides a `setup.py` script that build SimpleITK Python wheel. [SimpleITK](http://www.simpleitk.org) is a simplified programming layer on top of the [Insight Segmentation and Registration Toolkit](https://itk.org) (ITK).  ITK is an open-source, cross-platform system that provides developers with an extensive suite of software tools for image analysis.

## Automated wheels building with scripts

Steps required to build wheels on Linux, MacOSX and Windows have been automated. The
following sections outline how to use the associated scripts.

### Linux

On any linux distribution with `docker` and `bash` installed, running the script
`dockcross-manylinux-build-wheels.sh` will create 32 and 64-bit wheels for both
python 2.x and python 3.x in the `dist` directory.

For example:

```bash
$ git clone git://github.com/SimpleITK/SimpleITKPythonPackage.git
[...]

$ ./scripts/dockcross-manylinux-build-wheels.sh
[...]

$ ls -1 dist/
SimpleITK-0.11.0-cp27-cp27m-manylinux1_i686.whl
SimpleITK-0.11.0-cp27-cp27m-manylinux1_x86_64.whl
SimpleITK-0.11.0-cp27-cp27mu-manylinux1_i686.whl
SimpleITK-0.11.0-cp27-cp27mu-manylinux1_x86_64.whl
SimpleITK-0.11.0-cp33-cp33m-manylinux1_i686.whl
SimpleITK-0.11.0-cp33-cp33m-manylinux1_x86_64.whl
SimpleITK-0.11.0-cp34-cp34m-manylinux1_i686.whl
SimpleITK-0.11.0-cp34-cp34m-manylinux1_x86_64.whl
SimpleITK-0.11.0-cp35-cp35m-manylinux1_i686.whl
SimpleITK-0.11.0-cp35-cp35m-manylinux1_x86_64.whl
```

### MacOSX

*To be documented*

### Windows

*To be documented*

## Prerequisites

Building wheels requires:
* [CMake](https://cmake.org)
* Git
* C++ Compiler - Platform specific requirements are summarized in [scikit-build documentation](http://scikit-build.readthedocs.io).
* Python

## Detailed build instructions

### Building SimpleITK Python wheels

Build the SimpleITK Python wheel with the following command:

```
mkvirtualenv build-sitk
pip install -r requirements-dev.txt
python setup.py bdist_wheel
```

### Efficiently building wheels for different version of python

If on a given platform you would like to build wheels for different version of python, you can build the SimpleITK core libraries first and reuse them when building each wheel.

Here are the steps:

1. Build `SimpleITKPythonPackage` with `SimpleITKPythonPackage_BUILD_PYTHON` set to `OFF`

2. Build "flavor" of package using:

```
python setup.py bdist_wheel -- \
  -DSimpleITK_DIR:PATH=/path/to/SimpleITKPythonPackage-core-build/SimpleITK-superbuild/SimpleITK-build \
  -DSWIG_EXECUTABLE:PATH=/path/to/SimpleITKPythonPackage-core-build/SimpleITK-superbuild/Swig/bin/swig
```

## Miscellaneous
Written by Jean-Christophe Fillion-Robin from Kitware Inc.

It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0

For more information about SimpleITK, visit http://simpleitk.org

For more information about ITK, visit http://itk.org

