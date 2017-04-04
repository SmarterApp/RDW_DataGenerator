## README

**NOTE: recent changes to produce XML output may have broken existing functionality; don't expect the other output 
formats to work without some testing. Yeah, sorry about that but legacy output will be deprecated soon anyway.**

### What is this repository for? ###

This project generates sample data to be used in SBAC RDW project for functional testing.

### How do I get set up? ###

This is a Python 3 project and as such you will need Python 3 installed to use and/or develop the project.

To set up a virtual environment, execute the following command:

    virtualenv data-gen-env

> Where `data-gen-env` is the name of the directory where you want your environment files placed. 

You can activate the virtual environment with this command (_note that `data-gen-env` is the same name that was used 
with the creation of the environment. If you change the name of the environment in the first command, change it in 
this command too_):

    source data-gen-env/bin/activate

Once you have your environment activated (or you've decided not to use an environment), go into your repository and run
this command to finish setup:

    python setup.py develop

Note the use of `develop` in the call to `setup.py`. This will create a sym-link from the site-packages directory to the
working directory of your code. If instead you use `install`, it will copy the code and changes you make to the code
will probably not be picked up.

You will need `nose` to run the test suites. Along with those, we are using
[`coverage`](http://nedbatchelder.com/code/coverage/) for a unit testing code coverage report and
[`pep8`](http://pep8.readthedocs.org/en/latest/) as a style checker. If you have a virtual environment, run this within
it:

    pip install nose coverage pep8

Within the project is a suite of unit tests that cover a large percentage of the codebase. We are using `nose` for the
unit tests. To run the unit tests, start from the root of the project and call:

    nosetests test/*

As you develop new functionality, make sure to write accompanying unit tests so as maintain good code coverage and the
confidence that comes with it.

### How do I run it? ###

There are two scripts you can choose to run.

First script is `generate_data.py`. This generates the data in the requested output formats (can generate multiple formats at once).

> The following arguments apply:
> * `--state_name STATE_NAME`: Specify the name of the state that gets generated (defaults to `California)
> * `--state_code STATE_CODE`: Specify the code of the state that gets generated (defaults to `CA`)
> * `--state_type STATE_TYPE`: Specify the hierarchy type for the state to generate. 
This has to match configuration in in data_generator/config/state_type.py. Examples include `california`, `example` and `devel`. 

> Select what should be generated and output:
> * `--sum_pkg`: generate/load summative assessment (SUM) packages
> * `--ica_pkg`: generate/load interim comprehensive assessment (ICA) packages
> * `--iab_pkg`: generate/load interim assessment block (IAB) packages
> * `--gen_sum`: generate SUM outcomes
> * `--gen_ica`: generate ICA outcomes
> * `--gen_iab`: generate IAB outcomes
> * `--gen_item`: generate item level data (applies to both packages and outcomes)

> Select desired output:
> * `--pg_out`: Output data to a PostgreSQL database
> * `--star_out`: Output data to star schema CSV
> * `--lz_out`: Output data to landing zone CSV and JSON
> * `--xml_out`: Output data to (TRT) XML

> If using PostgreSQL output:
*(Note: with PostgreSQL the db schema must exists. Please refer to scripts/postgresql for more into)*

> * `--host`: Host for PostgreSQL server
> * `--schema`: Schema for PostgreSQL database

To run from IntelliJ, from the generate_data.py tab, select `Create 'generate_data'`, 
set the Script Parameters to, for example, `--state_type devel --gen_sum --xml_out`, verify the other settings and run.

The second script is `calculate_state_size.py`.
This will print out all the configured 'state_type's (from data_generator/state_type.py) and the stats for them.

### Outstanding open items  ###
1. Model: understand the concepts of Section and Staff. Do we need it? Also I do not like how InterimAssessment re-uses Assessment.
2. Understand if/how student groups are being generated.
3. Generators and sbac_generators: need to be combined and cleaned up, and better understood.
4. Config: most of it is self descriptive, but would be good to review and comment what each configuration means and how it is used.
5. WorkerManager - could be improved.
6. IDGen: need to remove the multithreading support. Also the whole concept of IDs generation could be cleaned up. 
7. When pointing to DB, it fails if you re-run it (with duplicate id constraint violation).It would be nice to be able to load the data incrementally.
8. There are some places with the explicit memory clean-up calls. Not sure if there is a problem with the memory utilization.
9. TODO in the code. 
10. By design, District/School names are random. That means that re-running the app generates different data (while the data volume is comparable).