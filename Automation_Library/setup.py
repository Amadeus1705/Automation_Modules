# setup.py
from setuptools import setup, find_packages

setup(
    name='Automation_modules_navi',
    version='0.1',
    packages=find_packages(),
    install_requires='requirements.txt',
    author='Suyash Sharma',
    author_email='suyashsharma.ds@gmail.com',
    description='A collection of automation modules for Navi Technologies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/Automation_modules_Navi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.6',
)