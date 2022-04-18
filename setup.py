from __future__ import print_function
from os import sys
from skbuild import setup

with open('SimpleITK/Readme.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='SimpleITK',
    version='2.1.1.2',
    author='Insight Software Consortium',
    author_email='insight-users@itk.org',
    packages=['SimpleITK'],
    package_dir={'SimpleITK':'SimpleITK'},
    download_url=r'https://www.itk.org/SimpleITKDoxygen/html/PyDownloadPage.html',
    description=r'SimpleITK is a simplified interface to the Insight Toolkit (ITK) for image registration and segmentation',
    long_description = long_description,
    long_description_content_type='text/markdown',
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
    keywords = 'SimpleITK ITK InsightToolkit segmentation registration',
    url = r'http://simpleitk.org/',
    project_urls={
        "Bug Tracker": "https://github.com/SimpleITK/SimpleITK/issues",
        "Documentation": "https://simpleitk.readthedocs.io/en/release/",
        "Source Code": "https://github.com/SimpleITK/SimpleITK",
    },
    install_requires=[],
    zip_safe=False
    )
