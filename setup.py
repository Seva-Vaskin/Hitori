import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = [x.strip() for x in f]

setuptools.setup(
    name="hitori",
    version="1.0",
    author="Diundina Maria",
    author_email="mary.diundina@gmail.com",
    description="Данное приложение является реализацией головоломки 'Хитори'.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.5",
)
