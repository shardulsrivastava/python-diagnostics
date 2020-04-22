from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='diagnostics-endpoint',
    version='0.0.7',
    description='Python package fo generating diagnostic endpoint for flask based python web applications.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Shardul Srivastava',
    author_email='shardul.srivastava007@gmail.com',
    keywords=['Flask', 'Endpoint', 'Diagnostics'],
    url='https://github.com/shardulsrivastava/python-diagnostics',
    download_url='https://pypi.org/project/diagnostics-endpoint/',
    include_package_data=True,
)

install_requires = [
    'flask', 'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
