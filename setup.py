from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Plant-e",
    version="0.0.1",
    author="DW Grp 5",
    author_email="author@example.com",
    description="This is to download the required files for RPi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoJunKai/DW-Plant-e.git",
    # packages=setuptools.find_packages(),
    py_modules = ["ave3", "database", "main"]
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
