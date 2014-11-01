"""
Docta is a new healing docs kit. Technically speaking, it's a static-site
generator slightly focused on building documetation.

Project homepage:
http://docta.05bit.com
"""
from setuptools import setup, find_packages

__version__ = '0.2.1'

install_requires=[
    'future',
    'misaka',
    # 'hoedown',  # seems unstable for now
    'watchdog',
    'jinja2',
    'PyYAML',
    'pygments',
    # 'docutils',
],

try:
    import argparse
except ImportError:
    install_requires.append('argparse')

setup(
    name="Docta",
    version=str(__version__),
    author="Alexey Kinyov",
    author_email='rudy@05bit.com',
    url='https://github.com/05bit/docta',
    description="Docta is a new healing docs kit.",
    long_description=__doc__,
    license='BSD',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points = {
        'console_scripts': 'docta = docta.cli:main'
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
    # use_2to3=True
)
