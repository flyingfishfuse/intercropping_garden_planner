
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
# requires python3-tk package be installed on debian buster
# requires:
# lxml
# flask-sqlalchemy
# pandas

setuptools.setup(
    name="Garden Plotter",
    version="0.0.1",
    author="Adam Galindo",
    author_email="author@example.com",
    description="Grid based planning for gardening/farming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)