from setuptools import setup, find_packages

setup(
    name="factory-feature",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain",
        "sentence-transformers",
        "ibm-watson-machine-learning",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "factory-feature=src.main:main",
        ],
    },
)
