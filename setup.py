"""
Docta is ...
"""
from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name='Docta',
    version=str(__version__),
    author='Alexey Kinyov',
    author_email='rudy@05bit.com',
    url='https://github.com/05bit/python-docta',
    description='A new documentation kit.',
    long_description=__doc__,
    license='BSD',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'future',
        'staticjinja',
        'hoedown', # misaka
        'watchdog',
        'docutils'
    ],
    entry_points = {
        'console_scripts': 'docta = docta.cli:main'
    },
    classifiers=[
        'Development Status :: 1 - Planning',
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
    use_2to3=True
)
