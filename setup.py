# Copyright (c) 2018 slumber1122 <slumber1122#gmail.com>.

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='consistent_hash',
    version='0.1',
    description="An implement of consistent hash with python",
    long_description=readme(),
    classifires=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Algorithm :: Consistent Hash'
    ],
    keywords="consistent hash",
    url='http://github.com/slumber1122/consistent-hash',
    author="slumber1122",
    author_email="slumber1122@gmail.com",
    license="MIT",
    packages=['consistent_hash'],
    install_requires=[],
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    include_package_data=True,
    zip_safe=False
)
