'''Setup script for silvair_tests_common_libs.'''

from setuptools import setup, find_packages

setup(
    name='aiowebcam',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'aiowebcam': [
            'static/*',
            'templates/*',
        ],
    },
    python_requires='>=3.6.0',
    install_requires=[
        'aiohttp>=3.3.2',
        'aiohttp-jinja2>=1.1.1',
        'docopt>=0.6.2',
        'Jinja2>=2.10.1',
    ],
    entry_points=dict(
        console_scripts=[
            'aiowebcam = aiowebcam.web:aiowebcam',
        ]
    ),
    author='Michał Lowas-Rzechonek',
    author_email='michal@rzechonek.net',
    license='MIT',
    url='http://rzechonek.net',
)
