# README #

### What is this repository for? ###

This folder contains scripts to create edware_ca schema in PostgreSQL database.

### How do I get set up? ###

To create edware_ca schema on edware db: 

    psql -h localhost -d edware -p 5432  -a -w -f  /Users/allagorina/development/dw_datagenerator/scripts/postgresql/edware.psql.sql
    
Load the data (replace the path with the appropriate path for your environment inside of the data load script as well as below):

    psql -h localhost -d edware -p 5432  -a -w -f  /Users/allagorina/development/dw_datagenerator/scripts/postgresql/edware.dataload.psql.sql