from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lux-builder',
    version='0.0.1',
    author="chenhui.lux.yu",
    author_email="chenhui.lux.yu@outlook.com",
    description="The origin purpose of this project is to build third party c++ project for lux framework project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'luxbuilder', 
        'luxbuilder.generators',
        'luxbuilder.getters'
    ],
    python_requies='>=3.8',
    install_requires=[
        'GitPython',
        'rich'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
 )
