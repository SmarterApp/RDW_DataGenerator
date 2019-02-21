# Notes about refactoring

* Configuration file.
* Data-driven subject and assessment definitions.
* Data-driven hierarchy.
* Refactor test generation flow control
* (?) Preserve generated data for subsequent runs

#### General

* Upgrade Python
* Improve project structure
* Code cleanup
    * replace % formatting with '{foo}'.format(foo=foo)
    * replace all * imports
    * use module/package scoping for all calls, i.e. `import modu` & `modu.sqrt` vs `from modu import sqrt` & `sqrt`
    * use pep8 to check conventions
* Improve CI
    * Have a (triggered) build that generates and publishes image
* Improve coverage a bit
* Should we have way to have embedded resources like Math_subject.xml available for loading?
* Clean up legacy output
    * (?) Do we want to keep a SQL output?
* Consider data volumes: Do we want to keep ability to generate huge amounts of data?
    * state_types


#### Configuration file

* Create model for configuration
    * Hierarchy: inline?, loaded, generated
        * For generated need params with pre-defined default sets
    * Subject(s): loaded
    * Assessment(s): loaded
    * Grades and school years: inline, derived from assessments
    * Testing schedule: inline (with defaults)
        * Includes which types of assessments and when
    * Group(s): generated (params)
* Command-line arguments will be mapped to configuration.
* Option to emit configuration (from defaults and command-line arguments)


#### Data-driven subject and assessment definitions

* Instead of having hard-coded configuration for known subjects, load the subject definition files and extract what is needed.
    * Add subject model
    * (?) Embed Math_subject.xml, ELA_subject.xml
* Remove assessment-generation code and only load from tabulator files.
    * (?) Embed assessments? If so, which years?


#### Data-driven hierarchy

Hierarchy is already data-driven but it is hard-coded config with hard-coded default sets.
* Change so hierarchy model has everything in it, with defaults.
    * (?) add testing schedule params
* Load/generate as specified.


#### Refactor test generation flow control

This is intended to capture the need to have a more class/group oriented generation strategy.
I think this will require introduction of classes in a set of students in a grade. This probably requires some params for controlling class size, etc.

To support:
* Groups of students (i.e. classes) taking assessments together, with make-up session(s)
* IABs throughout year
* ICAs twice a year (?) - at what level? school/subject? grade/subject? group?
* SUMs once a year at school/subject level


#### Preserve generated data

* Configuration.
    * During a run, save configuration file with all defaults, etc. Obviously don't overwrite source configuration file.
* Hierarchy. This is mostly in place, perhaps needs enhancing/cleanup.
* Students
    * Improve student model to include more capabilities, e.g. ELAS
    *
