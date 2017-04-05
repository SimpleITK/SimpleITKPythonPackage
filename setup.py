from __future__ import print_function
from os import sys
try:
    from skbuild import setup
except ImportError:
    try:
        from setuptools import setup
    except ImportError:
        print('setuptools or scikit-build is required to build from source.', file=sys.stderr)
        print('Please run:\n', file=sys.stderr)
        print('  python -m pip install setuptools')
        sys.exit(1)



setup(
    name='SimpleITK',
    version='1.0.0rc3',
    author='Insight Software Consortium',
    author_email='insight-users@itk.org',
    packages=['SimpleITK'],
    package_dir={'SimpleITK':'SimpleITK'},
    download_url=r'https://www.itk.org/SimpleITKDoxygen/html/PyDownloadPage.html',
    description=r'Simplified interface to the Insight Toolkit for image registration and segmentation',
    long_description='Provide an abstraction layer to ITK that enables developers\
    and users to access the powerful features of the InsightToolkit in a more \
    simplified manner.',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: C++",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
    license='Apache',
    keywords='ITK InsightToolkit segmentation registration image',
    url=r'http://simpleitk.org/',
    install_requires=[],
    setup_requires=['scikit-build>=0.5']
    )
