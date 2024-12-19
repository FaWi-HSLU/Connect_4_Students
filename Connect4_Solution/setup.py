from setuptools import setup, find_packages

"""
Installation of all required packages to run SenseHat
"""
setup(
    name='Connect4',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Flask',                # General Flask dependency
        'flask-swagger-ui',     # General Swagger UI for Flask
        'requests',             # Requests library for HTTP requests
        'numpy',                # Numpy for numerical operations
        'sense-hat'             # For the Raspi - Part
    ],
    python_requires='>=3.10, <4',
)

