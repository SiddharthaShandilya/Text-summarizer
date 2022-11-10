from tkinter.ttk import Notebook
from setuptools import setup
from typing import List

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str] = []

    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    return requirement_list
setup(
    name="src",
    version="0.0.1",
    author="siddhartha",
    description="A small package for text summary demo demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SiddharthaShandilya/Text-summarizer-heroku",
    author_email="siddharthashandilya104@gmail.com",
    packages=["src"],
    python_requires=">=3.7",
    install_requires=get_requirements(),
)