#!/bin/bash
set -e -x

# Build standalone project and populate archive cache
mkdir -p /work/standalone-build
pushd /work/standalone-build > /dev/null 2>&1
  cmake -DSimpleITKPythonPackage_BUILD_PYTHON:PATH=0 -G Ninja ../
  ninja
popd > /dev/null 2>&1

# Compile wheels re-using standalone project and archive cache
for PYBIN in /opt/python/*/bin; do
    if [[ ${PYBIN} == *"cp26"* ]]; then
        echo "Skipping ${PYBIN}"
        continue
    fi
    ${PYBIN}/pip install --user -r /work/requirements-dev.txt
    ${PYBIN}/python setup.py bdist_wheel -- \
      -DSimpleITK_DIR:PATH=/work/standalone-build/SimpleITK-superbuild/SimpleITK-build \
      -DSWIG_EXECUTABLE:PATH=/work/standalone-build/SimpleITK-superbuild/Swig/bin/swig
    ${PYBIN}/python setup.py clean
done

# Since there are no external shared libraries to bundle into the wheels
# this step will fixup the wheel switching from 'linux' to 'manylinux1' tag
for whl in dist/*.whl; do
    auditwheel repair $whl -w /work/dist/
    rm $whl
done

