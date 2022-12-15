import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Bb_rest_helper", 
    version="3.0.0",
    author="Javier Gregori",
    author_email="javier.gregori@anthology.com",
    description="A library to simplify requests to the Blackboard REST APIs for Anthology Blackboard products, alongside a bunch of convenience methods.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["Bb_rest_helper"],
    url="https://github.com/JgregoriBb/Bb_rest_helper",
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "requests>=2.24.0",
    ],
)