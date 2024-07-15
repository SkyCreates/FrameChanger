from setuptools import setup, find_packages

setup(
    name="framechanger",
    version="1.2.0",
    description="A wallpaper changer app that fetches images from TMDB",
    author="Akash Seam",
    author_email="akash.seam@gmail.com",
    url="https://github.com/SkyCreates/FrameChanger",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "requests",
        "PyQt5",
    ],
    entry_points={
        "console_scripts": [
            "framechanger=framechanger.app:run",
        ],
    },
    package_data={
        "framechanger": ["*.ico", "*.json", "*.py"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
