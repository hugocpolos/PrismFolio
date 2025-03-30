from setuptools import find_packages, setup

setup(
    name='prismfolio',
    packages=find_packages(include=['prismfolio']),
    version='0.1.0',
    description='To do',
    author='hugo.cpolos@gmail.com',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    include_package_data=True,
)
