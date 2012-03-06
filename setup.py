from setuptools import setup, find_packages

setup(
    name='gigs',
    version='0.1',
    url='http://github.com/shaunokeefe/gigs',
    license='BSD',
    description='Mock up for the Deakin gigs project',
    author="Shaun O'Keefe",
    author_email='shaun.okeefe.0@gmail.com',
    packages=find_packages(),
    package_dir= {'':'gigs'},
    install_requires=[
        'setuptools',
        ],
)
