from __future__ import print_function
from os import sys
from skbuild import setup


setup(
    name='SimpleITK',
    version='2.1.0',
    author='Insight Software Consortium',
    author_email='insight-users@itk.org',
    packages=['SimpleITK'],
    package_dir={'SimpleITK':'SimpleITK'},
    download_url=r'https://www.itk.org/SimpleITKDoxygen/html/PyDownloadPage.html',
    description=r'SimpleITK is a simplified interface to the Insight Toolkit (ITK) for image registration and segmentation',
    long_description =r'SimpleITK provides an abstraction layer to ITK that enables developers \
                        and users to access the powerful features of the InsightToolkit in an easy \
                        to use manner for biomedical image analysis.',
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
    keywords='SimpleITK ITK InsightToolkit segmentation registration',
    url=r'https://simpleitk.org/',
    install_requires=[],
    zip_safe=False
    )
