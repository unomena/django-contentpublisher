from setuptools import setup, find_packages

setup(
    name='django-contentpublisher',
    version='0.1.0',
    description='Django qa publishing app.',
    long_description = open('README.rst', 'r').read(),
    author='Unomena',
    author_email='dev@unomena.com',
    license='BSD',
    packages = find_packages(),
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)