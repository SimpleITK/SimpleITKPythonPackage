from skbuild import setup

setup(
    name='SimpleITK',
    version='0.11.0',
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
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering"
        ],
    license='Apache',
    keywords='ITK InsightToolkit segmentation registration image',
    url=r'http://simpleitk.org/',
    install_requires=[
    ]
    )
