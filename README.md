# SimpleITKPythonPackage

This project provides a `setup.py` script that build SimpleITK Python wheel. [SimpleITK](http://www.simpleitk.org) is a simplified programming layer on top of the [Insight Segmentation and Registration Toolkit](https://itk.org) (ITK).  ITK is an open-source, cross-platform system that provides developers with an extensive suite of software tools for image analysis.

## Building the SimpleITK Python wheel module

Building the wheel requires:
* [CMake](https://cmake.org)
* Git
* C++ Compiler
* Python

Build the SimpleITK Python wheel with the following command:

```
mkvirtualenv build-sitk
pip install -r requirements-dev.txt
python setup.py bdist_wheel
```

## Efficiently building wheels for different version of python

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
Written by Jean-Christophe Fillion-Robin from the Kitware Inc.

It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0

For more information about SimpleITK, visit http://simpleitk.org

For more information about ITK, visit http://itk.org

