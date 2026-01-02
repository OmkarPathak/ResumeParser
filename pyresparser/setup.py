from setuptools import setup, find_packages

setup(
    name='pyresparser',
    version='1.1.0',
    description='A simple resume parser used for extracting information from resumes',
    url='https://github.com/OmkarPathak/pyresparser',
    author='Omkar Pathak',
    author_email='omkarpathak27@gmail.com',
    license='GPL-3.0',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'nltk',
        'spacy',
        'pandas',
        'docx2txt',
        'pdfminer.six',
    ],
)
