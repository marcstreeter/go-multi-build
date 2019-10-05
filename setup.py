from setuptools import setup

setup(
    name="guilder",
    version="0.1",
    py_modules=['tasks'],
    install_requires=['invoke'],
    entry_points={
        'console_scripts': ['guilder = guilder.main:program.run']
    }
)