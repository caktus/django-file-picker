from setuptools import setup, find_packages

packages = find_packages()
packages.remove('sample_project')
setup(
    name='django-file-picker',
    version='0.0.0',
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['*.sql', '*.pyc'],
    },
    url='http://bitbucket.org/copelco/django-file-picker/',
    license='LICENSE.txt',
    description='Pluggable file picker',
    long_description=open('README.rst').read(),
)
