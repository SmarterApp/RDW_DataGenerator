## README

**NOTE: recent changes to produce XML output may have broken existing functionality; don't expect the other output 
formats to work without some testing. Yeah, sorry about that but legacy output will be deprecated soon anyway.**

This project generates sample data to be used in SBAC RDW project for functional testing.

### How do I run it?

There are two scripts you can choose to run. See CONTRIBUTING.md for instructions for running them directly. 
Otherwise use the docker image to run the generate script.

First script is `generate_data.py`. This generates the data in the requested output formats (can generate multiple formats at once).

> The following arguments apply:
> * `--state_name STATE_NAME`: Specify the name of the state that gets generated (defaults to `California`)
> * `--state_code STATE_CODE`: Specify the code of the state that gets generated (defaults to `CA`)
> * `--state_type STATE_TYPE`: Specify the hierarchy type for the state to generate. 
This has to match configuration in in data_generator/config/state_type.py. Examples include `california`, `example` and `devel`. 

> Select what should be generated and output:
> * `--sum_pkg`: generate/load summative assessment (SUM) packages
> * `--ica_pkg`: generate/load interim comprehensive assessment (ICA) packages
> * `--iab_pkg`: generate/load interim assessment block (IAB) packages
> * `--pkg_source`: either `generate` (default) or path where tabulator CSV files are located
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

The second script is `calculate_state_size.py`.
This will print out all the configured 'state_type's (from data_generator/state_type.py) and the stats for them.
Current output looks like:
```text
Calculating for type: devel
    Districts: 4
    Schools  : 24
    Students : 8600
Calculating for type: udl_test
    Districts: 1
    Schools  : 200
    Students : 200000
Calculating for type: pa
    Districts: 102
    Schools  : 5184
    Students : 2017200
Calculating for type: tiny
    Districts: 2
    Schools  : 12
    Students : 182
Calculating for type: example
    Districts: 13
    Schools  : 264
    Students : 109475
Calculating for type: california
    Districts: 1011
    Schools  : 16150
    Students : 7033000
```
The number of test results produced depends on the distribution of the students, which assessment types are enabled
and which years results are generated for. Using the default 2015, 2016, 2017 you can expect per student, about:
```text
SUM - 6 
ICA - 18
IAB - 147, weighted average of ~130 for grades 3-8, ~230 for grade 11
```
Call it 170 per student over the three years. So, `example` produces > 18 million results; `california` > 1.2 billion! 

Obviously, the size of the output depends on the format:
* XML with item data ~ 18k per file

### How do i run the docker image?
When running the image, pass the data generation parameters:

    docker run fwsbac/rdw-datagen --state_type tiny --gen_iab --gen_item --xml_out

To get at the resulting data you need to either map a local folder:

    docker run -v ~/out:/src/data_generator/out fwsbac/rdw-datagen ...

Or use docker to find where it mapped the folder (NOTE: Docker for Mac adds another layer of abstraction so you'll
have to dig even deeper to find the actual data bits):

    # get CONTAINER ID of instance that is now exited
    docker ps -a
    docker inspect --format '{{.Mounts}}' <CONTAINER ID>

#### Setting up an EC2 instance with docker
Followed the directions from: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html.
Create EC2 instance using Amazon Linux or CentOS image. Then ...

    sudo yum update -y
    sudo yum install -y docker
    sudo service docker start
    sudo usermod -a -G docker ec2-user     <-- have to relog to be in group
    docker info
    mkdir out
    docker run -v ~/out:/src/data_generator/out fwsbac/rdw-datagen --state_type tiny --gen_iab --gen_item --xml_out