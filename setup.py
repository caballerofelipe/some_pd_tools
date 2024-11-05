from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='some_pd_tools',
    version='1.0.3',
    description='Some tools to be used with Pandas.',
    package_dir={'': 'packages'},
    packages=find_packages(where='packages'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/caballerofelipe/some_pd_tools',
    author='Felipe Caballero',
    # author_email='mail@mail.mail',
    license='GPL-3.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=['pandas>=2'], # Might need review
    extras_require={
        'dev': ['pytest', 'twine', 'build'],
        # 'save_load': ['pytables>=3'],
    },
    python_requires='>=3.4',
)
