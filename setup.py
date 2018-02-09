#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zoosrv',
    version="0.1.3",
    description=(
        'Python Servers for Distributed Zeroth-Order Optimization'
    ),
    author='Yang Yu',
    author_email='yuy@nju.edu.cn',
    maintainer='Yu-Ren Liu, Yang Yu',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/eyounx/ZOOsrv',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'ConfigParser',
        'liac-arff'
    ]
)
