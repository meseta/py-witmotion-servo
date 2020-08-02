import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-witmotion-servo",
    version="1.0.0",
    author="Yuan Gao",
    author_email="github@meseta.dev",
    description="Driver for Witmotion Servo Controller boards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meseta/py-witmotion-servo",
    packages=setuptools.find_packages(),
    install_requires=[
        "hidapi==0.9.0.post3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)