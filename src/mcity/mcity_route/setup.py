#!/usr/bin/env python3

from setuptools import setup, find_packages

package_name = 'mcity_route'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    zip_safe=True,
    maintainer='Zhijie Qiao',
    maintainer_email='zhijieq@umich.edu',
    description='The mcity_route package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mcity_route_sim = mcity_route.mcity_route_sim:main',
            'mcity_route_realcar = mcity_route.mcity_route_realcar:main',
        ],
    },
)