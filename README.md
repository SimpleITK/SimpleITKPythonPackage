# SimpleITKPythonPackage

This project provides a modern build system using [scikit-build-core](https://scikit-build-core.readthedocs.io/) to build, install, and package SimpleITK for Python. [SimpleITK](http://www.simpleitk.org) is a simplified programming layer on top of the [Insight Segmentation and Registration Toolkit](https://itk.org) (ITK). ITK is an open-source, cross-platform system that provides developers with an extensive suite of software tools for image analysis.

SimpleITK is available for binary downloads from [PyPI](https://pypi.python.org/pypi/SimpleITK) for many common platforms. Also a source distribution is available of this repository which may be used when an appropriate binary [wheel](http://pythonwheels.com) is not available.

To install SimpleITK:

```bash
python -m pip install SimpleITK
```

## Installing SimpleITK for Python from the Python Packaging Source

```bash
python -m pip install --no-binary SimpleITK SimpleITK
```

### Prerequisites

The build requirements are specified in the `pyproject.toml` file via [PEP 518](https://peps.python.org/pep-0518/). The requirements should be automatically downloaded when using a [PEP 517](https://peps.python.org/pep-0517/) compliant build front-end like `pip` or `build`.

Additionally building *requires*:
* Git
* C++ Compiler - Platform specific requirements are summarized in [scikit-build-core documentation](https://scikit-build-core.readthedocs.io/)
* Python >= 3.10
  
Please ensure that `pip` is up to date.

```bash
python -m pip install --upgrade pip
```

## Detailed build instructions

### Building SimpleITK Python wheels

Build the SimpleITK Python wheel with the following command:

To build only a wheel (not sdist):

```bash
python -m build --wheel
```

### Building Source Distribution

The Python [build](https://pypa-build.readthedocs.io/en/latest/) package should be used to build the source distribution:

```bash
python -m build --sdist
```

### Configuration Options

You can pass configuration options to the build using `-C` or `--config-settings`:

```bash
# Enable verbose build output
python -m build -C build.verbose=true

# Set CMake build type
python -m build -C cmake.build-type=Debug

# Pass CMake defines
python -m build -C cmake.define.SOME_OPTION=ON

# Use a persistent build directory for faster rebuilds
python -m build -C build-dir=build
```

For more configuration options, see the [scikit-build-core documentation](https://scikit-build-core.readthedocs.io/en/latest/configuration/index.html).

### Efficiently building wheels for different versions of Python

If on a given platform you would like to build wheels for different versions of Python, you can build the SimpleITK core libraries first and reuse them when building each wheel.

Here are the steps:

1. Build `SimpleITKPythonPackage` with `SimpleITKPythonPackage_BUILD_PYTHON` set to `OFF`:

```bash
python -m build -C build-dir=build -Ccmake.define.SimpleITKPythonPackage_BUILD_PYTHON=OFF
```

2. Build wheels for different Python versions by passing the pre-built paths via config settings:

```bash
python3.10 -m build --wheel -C cmake.define.SimpleITK_DIR=/path/to/build/sitk-sb/SimpleITK-build \
  -C cmake.define.ITK_DIR=/path/to/build/sitk-sb/ITK-build

python3.11 -m build --wheel -C cmake.define.SimpleITK_DIR=/path/to/build/sitk-sb/SimpleITK-build \
  -C cmake.define.ITK_DIR=/path/to/build/sitk-sb/ITK-build

```

### Development and Editable Installs

For development, you can install SimpleITK in editable mode:

```bash
pip install -e . --no-build-isolation
```

For faster rebuilds during development, use a persistent build directory:

```bash
pip install -e . --no-build-isolation -C build-dir=build
```

For more information on editable installs, see the [scikit-build-core editable documentation](https://scikit-build-core.readthedocs.io/en/latest/configuration/index.html#editable-installs).

## Build System

This package uses [scikit-build-core](https://scikit-build-core.readthedocs.io/), a modern Python build backend that uses CMake. Key features include:

- **Automatic dependency management**: CMake and Ninja are automatically provided if needed
- **PEP 517/518 compliant**: Works with modern Python build tools
- **Configurable**: Extensive configuration options via `pyproject.toml` or command-line
- **Cross-platform**: Supports Windows, macOS, and Linux
- **Fast rebuilds**: Optional persistent build directories for development

### Available CMake Options

The following CMake options can be set via config settings:

- `SimpleITKPythonPackage_BUILD_PYTHON`: Build Python bindings (default: ON)
- `SimpleITK_PYTHON_THREADS`: Enable threaded Python usage by unlocking the GIL (default: ON)
- `SimpleITK_PYTHON_USE_LIMITED_API`: Use Python Limited API for minor version compatibility (default: ON for Python >= 3.11)
- `SimpleITK_DIR`: Path to existing SimpleITK build directory (for reusing builds)
- `USE_CCACHE`: Enable ccache for faster rebuilds (default: OFF)

Example:

```bash
python -m build -C cmake.define.SimpleITK_PYTHON_THREADS=OFF \
                -C cmake.define.USE_CCACHE=ON
```

## Miscellaneous
Written by Jean-Christophe Fillion-Robin from Kitware Inc. and Bradley Lowekamp.

It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0

For more information about SimpleITK, visit http://simpleitk.org

For more information about ITK, visit http://itk.org

