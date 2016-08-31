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
pip install -r requirements.txt
python setup.py bdist_wheel
```

## Miscellaneous
Written by Jean-Christophe Fillion-Robin from the Kitware Inc.

It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0

For more information about SimpleITK, visit http://simpleitk.org

For more information about ITK, visit http://itk.org

