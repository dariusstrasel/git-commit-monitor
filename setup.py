from distutils.core import setup

setup(
    name='git-commit-monitor',
    version='0.0.0',
    packages=['git-commit-monitor'],
    install_requires=['requests'],
    url='www.dariusstrasel.com',
    license='MIT',
    author='Darius Strasel',
    author_email='strasel.darius@gmail.com',
    description='A script to grab number of commits created by a user for the day.'
)
