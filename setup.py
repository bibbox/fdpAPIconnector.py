import setuptools
import os

path_wd = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
with open(os.path.join(path_wd,'src','fdpAPIconnector', '__version__.py')) as f:
    exec(f.read(), version)

setuptools.setup(
    name="fdpAPIconnector",
    version=version['__version__'],
    author="Emilian Jungwirth",
    author_email="emilian.jungwirth@medunigraz.at",
    description="Python package to connect to a FDP API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bibbox/fdpAPIconnector.py",
    install_requires=['rdflib',
                      'requests'],
    project_urls={
        "Bug Tracker": "https://github.com/bibbox/fdpAPIconnector.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)