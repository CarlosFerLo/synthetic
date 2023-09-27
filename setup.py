from distutils.core import setup
from setuptools import find_packages
import os


setup(
    name="synthetic-cognition",
    version="{{VERSION_PLACEHOLDER}}" if os.environ["ENV"] == "PROD" else "0.0.1",
    description="Synthetic Cognition general inference architecture for language model agents DEMO",
    packages=find_packages("."),
    long_description="Synthetic Cognition general inference architecture for language model agents DEMO",
    author="Carlos Fernández Lorán",
    author_email="carlos.ferlo6165@gmail.com",
    fullname="Synthetic Cognition",
    keywords=["language models", "inference", "agents", "autonomous", "llm"],
)