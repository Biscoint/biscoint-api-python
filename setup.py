import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biscoint-api-python",
    version="0.5.1",
    author="Thiago Borges Abdnur",
    author_email="bolaum@gmail.com",
    description="Biscoint API wrapper for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Biscoint/biscoint-api-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires='>=3.6',
)
