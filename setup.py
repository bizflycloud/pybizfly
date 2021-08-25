import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybizfly",  # Replace with your own username
    version="0.2.0",
    author="BizFly Cloud",
    author_email="dungpq@vccloud.vn",
    description="BizFly Client in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bizflycloud/pybizfly",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.24.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU AFFERO GENERAL PUBLIC LICENSE",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
