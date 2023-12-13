from setuptools import setup, find_packages


setup(
    name='zeit.nightwatch',
    version='1.7.1',
    author='Zeit Online',
    author_email='zon-backend@zeit.de',
    url='https://github.com/ZeitOnline/zeit.nightwatch',
    description='pytest helpers for http smoke tests',
    long_description='\n\n'.join(
        open(x).read() for x in ['README.rst', 'CHANGES.txt']),
    namespace_packages=['zeit'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    install_requires=[
        'cssselect',
        'lxml',
        'mechanicalsoup',
        'requests',
        'prometheus_client',
        'pytest',
        'pytest-playwright',
        'selenium',
        'setuptools',
    ],
    entry_points={
        'pytest11': ['zeit_nightwatch=zeit.nightwatch.pytest'],
    }
)
