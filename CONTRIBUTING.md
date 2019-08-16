## RDW_DataGenerator for Contributors

This document is targeted at developers contributing to the RDW_DataGenerator project.

### Version Control Conventions
Repo: https://github.com/SmarterApp/RDW_DataGenerator

This project follows the common convention of having two main branches with infinite lifetime: `master` is the main
branch where HEAD contains the production-ready state, while `develop` is the main branch where HEAD contains the 
latest changes for the next release.
 
Use feature branches off of `develop` for all new features. Use a prefix of `feature/` to highlight those branches.
For example, the new shoesize feature work would be in `feature/shoesize`. Create pull requests from the feature
branch to `develop` to solicit code reviews and feedback. Once approved use `squash and merge` into `develop`.


### How do I get set up?
This is a Python 3 project and as such you will need Python 3 installed to develop the project.
As of early 2019, the project uses 3.7.2.

To set up a virtual environment, execute the following command where `venv-datagen` is the name of the directory where you want your environment files placed.
```bash
python3 -m venv venv-datagen
```

You can activate the virtual environment with this command (_note that `venv-datagen` is the same name that was used with the creation of the environment. If you change the name of the environment in the first command, change it in this command too_):
```bash
source venv-datagen/bin/activate
python --version
```

Once you have your environment activated (or you've decided not to use an environment), go into your repository and run this command to finish setup:
```bash
pip install -r requirements-dev.txt
```

To run the test suites with coverage (and PEP8 checking if desired):
```bash
# just run coverage with results in console
pytest --cov=datagen tests/
# add PEP8 checking - but this is checking the test code for compliance
pytest --cov=datagen --pep8 tests/
# generate a nice html report
pytest --cov-report html:coverage --cov=datagen tests/
```

You can use pytest to test PEP8 on source (`pytest.ini` is configured to hide some warnings):
```bash
pytest --pep8 datagen/
```

As you develop new functionality please keep the test coverage and PEP8-compliance up.

### Running

The README outlines how to run the generator using docker. As a developer you will want to run the generator from
the IDE. To run from IntelliJ, from the generate_data.py tab, select `Create 'generate_data'`, set the Script
Parameters to, for example, `--state_type devel --gen_sum --xml_out`, verify the other settings and run/debug.

You may also invoke the script on the command line with appropriate arguments (see README.md for details on arguments).
From the root project folder, for example:
```bash
python -m datagen.generate_data --gen_sum --xml_out --pkg_source ./in/src/*.ELPAC.csv --hier_source ./in/pern.csv
```


### Building

The artifact for this project is a docker image. No eggs or wheels or anything like that.
Assuming you have Docker installed and DockerHub configured, you can build and push the image:
```bash
docker build -t fwsbac/rdw-datagen:latest .
docker push fwsbac/rdw-datagen
```

Refer to README.md for instructions for running the docker image.

#### CI Build

The CI system uses docker to build the build environment. If you want to replicate it do something like:
```bash
find . -name "*.pyc" -o -name "__pycache__" -delete
docker build -f Dockerfile.dev -t datagen-dev .
docker run -v `pwd`:/out datagen-dev pytest --cov-report html:/out/coverage --cov=datagen tests/
```

#### Troubleshooting the Docker Image
If things aren't working properly and you want to get into the image, you can override the entrypoint. Comment out the
ENTRYPOINT and CMD lines in `Dockerfile` and replace with:
```
CMD ["python", "-m", "datagen.generate_data", "--help"]
```
Then you can run the image with the shell:
```bash
docker run -it fwsbac/rdw-datagen /bin/sh
```


### Tasks
This project was originally created to generate data for the legacy reporting data warehouse. It was modified to 
generate data for the new system, mostly to take advantage of the good demographics generation. As such there are a 
number of things that may need cleaning up. And there are some enhancements/improvements. In no particular order:

 - [ ] Occasionally a (summative?) test result should be missing target scores
 - [ ] Use only a subset of items from item bank in a particular session outcome (?)
 - [ ] Combine cfg.DEMOGRAPHICS_BY_GRADE and population.DEMOGRAPHICS. They both represent demographic distribution of
 students but they have different values.
 - [ ] How are Section/Staff used? Can they be removed? Consider the session-based generation task.
 - [ ] Stage work to avoid memory utilization problems for large generations.
 - [ ] Rare admin condition exceptions. Summative: IN, perhaps by session. ICA: NS, perhaps by school.
 - [ ] Rare status exceptions. Instead of "scored": "appeal", "paused", "reset". Careful, they have meanings.
 - [ ] Rare completeness/completeStatus exceptions. "partial" instead of "complete". Work in forceComplete.
 - [ ] Rare unscored tests.
 - [ ] Change student attributes when they advance. For example LEP/ELAS, IEP.
 - [ ] Correlate certain attributes. For example, all ELPAC students should have LEP=Yes, ELAS=EL.
 - [ ] Address date-taken requests (see \* below)

\* Currently there is a single date-taken per assessment per school/grade. This isn't particularly realistic but does
force all students in a group to have the same date-taken so they have the same session (session name is based on
date-taken and group name). The ask is to have all students in a group have the same session with 0-3 students of the
group in a second session, sometimes. Then the date-taken for a school/grade should be spread out, not all the same day.
Perhaps use school attributes to control when assessments are given.
