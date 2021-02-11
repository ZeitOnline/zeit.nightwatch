from setuptools import setup, find_packages


setup(
    name='zeit.nightwatch',
    version='1.0.0.dev0',
    author='Zeit Online Backend',
    author_email='zon-backend@zeit.de',
    description='',
    long_description=(
        open('README.rst').read() +
        '\n\n' +
        open('CHANGES.txt').read()),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='GPL v2',
    install_requires=[
        'cssselect',
        'lxml',
        'mechanicalsoup',
        'requests',
        'pytest',
        'setuptools',
    ],
    entry_points={
        'pytest11': ['zeit_nightwatch=zeit.nightwatch.pytest'],
    }
)
