import setuptools
import slicey

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slicey",
    version=slicey.__version__,
    author="TG-Techie (Jonah Y-M)",
    author_email="tgtechie01@gmail.com",
    description="Add Mutating Slices to Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TG-Techie/slicey",
    py_modules=["slicey"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
