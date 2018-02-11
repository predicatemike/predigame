from setuptools import setup, find_packages

setup(
    name = 'predigame',
    version = '0.8.7',
    description = 'A Python based game development platform',
    url = 'http://predicate.us',
    author = 'Predicate Academy',
    author_email = 'info@predicate.us',
    packages = find_packages(),
    install_requires = ['pygame'],
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'pigm = predigame:main'
        ]
    }
)
