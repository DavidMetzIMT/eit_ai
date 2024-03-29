"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


setup(
    name="eit_ai",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.0.1",
    description="Tensorflow/Keras workspace for ",
    url="https://github.com/DavidMetzIMT/eit_ai",
    # Author details
    author="David Metz",
    author_email="david.metz67@gmail.com",
    # Choose your license
    license="MIT License",
    # What does your project relate to?
    keywords="python tools for electrical impedance tomography ",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["test", "datasets", "outputs", "_test_scripts"]),
    zip_safe=False,
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('pyeit', ['data/data_file'])],
)