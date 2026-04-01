from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="reveal-nlp",
    version="0.2.0",
    author="Bonnie Bingham",
    description="Open-source Python library for intelligent harm detection and linguistic analysis in text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bbplus3/reveal",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "reveal": ["dictionaries/*.json"],
    },
    install_requires=[
        "nltk>=3.8",
        "textblob>=0.17",
        "scikit-learn>=1.0",
        "numpy>=1.19",
        "pandas>=1.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.9",
    keywords="nlp harm-detection linguistic-analysis cryptanalysis propaganda sentiment",
)