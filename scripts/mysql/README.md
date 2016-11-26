# README #

### What is this repository for? ###

This folder contains scripts to load the data generate using `--star_out` (output data to star schema CSV) into MySQL database.

### How do I get set up? ###

Install MySQL.

Create a database to load the data. For example:
 
    mysql> create edware db;

Connect to the database using `--local-infile` option:

    mysql --local-infile edware

First create tables (replace the path with the appropriate path for your environment):
    mysql> source /Users/allagorina/development/edware.mysql.sql

Edit mysql.dataload.sql by replacing the path with he appropriate path for your environment.

Load the data (replace the path with the appropriate path for your environment):

    mysql> source /Users/allagorina/development/edware.dataload.mysql.sql