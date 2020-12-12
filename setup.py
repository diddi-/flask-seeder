import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Flask-Seeder",
    version="1.2.0",
    url="https://github.com/diddi-/flask-seeder",
    author="Diddi Oskarsson",
    author_email="diddi@diddi.se",
    description="Flask extension to seed database through scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="MIT",
    install_requires=[
        "Flask>=1.0.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "flask.commands": [
            "seed=flask_seeder.cli:seed",
        ]
    }
)
