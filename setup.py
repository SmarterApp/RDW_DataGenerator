import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = ['psycopg2 == 2.5.1', 'pyprind == 2.9.9']

tests_require = requires + ['nose',
                            'pep8',
                            'coverage']

private_repositories = ['lib']

setuptools.setup(name='DataGeneration',
                 version='0.2',
                 description='Data generator for the SBAC RDW project',
                 author='Fairway Technolgies',
                 author_email='',
                 maintainer='Fairway Technolgies',
                 maintainer_email='',
                 license='proprietary',
                 url='',
                 classifiers=['Programming Language :: Python', 'Programming Language :: Python :: 3.3',
                              'Operating System :: OS Independent', 'Intended Audience :: Developers',
                              'Topic :: Education', 'Topic :: Software Development :: Quality Assurance',
                              'Topic :: Software Development :: Testing', 'Topic :: Utilities'],
                 keywords='data generation education SBAC',
                 packages=['data_generator',
                           'data_generator.config',
                           'data_generator.generators',
                           'data_generator.model',
                           'data_generator.util',
                           'data_generator.writers'],
                 zip_safe=False,
                 test_suite='nose.collector',
                 install_requires=requires,
                 tests_require=tests_require,
                 dependency_links=private_repositories,
                 entry_points='')
