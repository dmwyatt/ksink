import pathlib

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    long_description=README,
    long_description_content_type='text/markdown',
    name='ksink',
    version='0.1.1',
    description='A simple tool for copying files with a nice progress bar.',
    url='https://github.com/dmwyatt/ksink',
    python_requires='==3.*,>=3.8.0',
    author='Dustin Wyatt',
    author_email='dustin.wyatt@gmail.com',
    license='MIT',
    packages=['ksink'],
    install_requires=[],
    extras_require={"dev": ["wheel==0.*,>=0.34.2"]},
    entry_points={
        "console_scripts": [
            "ksink = ksink.cli:transfer"
        ]
    }
)
