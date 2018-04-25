from setuptools import find_packages, setup

setup(
    name='strangelove',
    version='0.0.1',
    author='Strangelove Authors',
    license='MIT',
    description='Collabrative Filtering for Movie Datasets',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    include_package_data=True,
    package_data={
        '': ['*.csv', '*.md'],
    },
    keywords='Collabrative Filtering, Recommendation Systems',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=open('requirements.txt').read().splitlines(),
    url='https://github.com/gokcan/strangelove')
