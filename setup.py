from setuptools import setup

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    with open("Readme.md", 'r') as f:
        long_description = f.read()

setup(
    name='tkTimePicker',
    version='2.0.1',
    description='This package provides you with easy to customize timepickers',
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Paul',
    url="https://github.com/PaulleDemon/tkTimePicker",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    keywords=['tkinter', 'timepicker', 'time', 'tktimepicker'],
    packages=["tktimepicker"],
    include_package_data=True,
    python_requires='>=3.6',
)
