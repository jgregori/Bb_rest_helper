import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Bb_rest_helper", 
    version="1.1.2",
    author="Javier Gregori",
    author_email="javier.gregori@blackboard.com",
    description="A Python 3 library to simplify working with Blackboard APIs.",
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
        "jwt==1.0.0",
        "PyJWT==1.7.1",
        "requests==2.24.0",
    ],
)