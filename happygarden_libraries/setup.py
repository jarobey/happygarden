from setuptools import setup, find_packages
from happygarden import VERSION

setup(
    name="happygarden",
    version=VERSION,
    description="Jason Robey's work to manage his garden (in the British sense of the word)",
    url='https://github.com/jarobey/happygarden',
    author='Jason Robey',
    author_email='jason@robeydespain.net',
    zip_safe=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)