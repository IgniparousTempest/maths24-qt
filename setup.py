import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maths24-qt", # Replace with your own username
    version="0.9",
    author="Courtney Pitcher",
    author_email="cr.pitcher@gmail.com",
    description="A maths puzzle game where the objective is to use arithmetic to make the number 24",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IgniparousTempest/maths24-qt",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'gui_scripts': ['maths24-qt = maths24.main:main']
    },
    data_files = [
        ('share/applications/', ['maths24.desktop'])
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)