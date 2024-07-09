from setuptools import setup, find_packages

setup(
    name="framechanger",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pyqt5",
    ],
    entry_points={
        "console_scripts": [
            "framechanger=framechanger.app:run",
        ],
    },
    package_data={
        "framechanger": ["icon.ico"],
    },
    author="Akash Seam",
    author_email="akash.seam@gmail.com",
    description="A wallpaper changer app that fetches images from TMDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SkyCreates/FrameChanger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
