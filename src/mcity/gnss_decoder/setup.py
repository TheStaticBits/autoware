from setuptools import setup
import os
from glob import glob

package_name = 'gnss_decoder'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zhijie Qiao',
    maintainer_email='zhijieq@umich.edu',
    description='GNSS decoder node for processing IMU, odometry, and GNSS data',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gnss_decoder = gnss_decoder.gnss_decoder:main',
        ],
    },
) 