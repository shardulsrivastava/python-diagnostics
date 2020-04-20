from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='diagnostics-endpoint',
    version='0.0.5',
    description='Python package for a diagnostics endpoint',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Shardul Srivastava',
    author_email='shardul.srivastava@rea-group.com',
    keywords=['Flask', 'Endpoint', 'Diagnostics'],
    include_package_data=True,
)

install_requires = [
    'flask', 'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
