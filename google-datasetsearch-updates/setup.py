import pathlib
import setuptools
from setuptools import setup

PATH = pathlib.Path(__file__).parent

# The text of the README file
README = (PATH / "README.md").read_text()

setup(
    name = "google-datasetsearch-updates",
    version = "0.0.1",
    author = "Jules Rostand",
    author_email = "jules.rostand@outlook.com",
    description = ("Enregistrer l'historique des mises à jour de base de données recensées sur le service Data Set Search de Google."),
    long_description=README,
    long_description_content_type="text/markdown",
    url = "https://github.com/j-rostand/google-datasetsearch-updates",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
