from setuptools import setup, find_packages
import sys

setup(
    name='garpix-catalog',
    version='0.0.1',
    description='Garpix catalog package',
    author='Garpix LTD',
    author_email='info@garpix.com',
    license='Commercial',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Commercial',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >= 2.0',
    ],
)
