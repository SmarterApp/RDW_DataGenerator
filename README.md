# README #

### What is this repository for? ###

This project generates sample data to be used in SBAC RDW project for functional testing.

### How do I get set up? ###

This is a Python 3 project and as such you will need Python 3 installed to use and/or develop the project.

To set up a virtual environment, execute the following command:

    virtualenv data-gen-env

> Where `data-gen-env` is the name of the directory where you want your environment files placed. 

You can activate the virtual environment with this command:

    source data-gen-env/bin/activate

Note that `data-gen-env` is the same name that was used with the creation of the environment. If you change the name of
the environment in the first command, change it in this command too.

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
> * `--state_type STATE_TYPE`: Specify the hierarchy type for the state to generate. This has to match configuration in in data_generator/state_type.py 
> * `--pg_out`: Output data to a PostgreSQL database
> * `--star_out`: Output data to star schema CSV
> * `--lz_out`: Output data to landing zone CSV and JSON
> * `--io`: Output item-level data
> * `--gia`: Generate interim assessment blocks

> If using PostgreSQL output:
*(Note: with PostgreSQL the db schema must exists. Please refer to scripts/postgresql for more into)*

> * `--host`: Host for PostgreSQL server
> * `--schema`: Schema for PostgreSQL database

The second script is `calculate_state_size.py`.
This will print out all the configured 'state_type's (from data_generator/state_type.py) and the stats for them.