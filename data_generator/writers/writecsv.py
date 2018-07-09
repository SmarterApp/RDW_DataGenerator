"""
This is the general CSV writer.

"""

import csv
import os
import shutil

import data_generator.writers.util as writers_util
from data_generator.writers.datefilters import FILTERS as DATE_TIME_FILTERS
from data_generator.writers.filters import ALL_FILTERS as FILTERS

available_filters = DATE_TIME_FILTERS.copy()
available_filters.update(FILTERS)


def clean_dir(out_path_root):
    # Verify output directory exists
    if not os.path.exists(out_path_root):
        os.makedirs(out_path_root)

    # Clean output directory
    for file in os.listdir(out_path_root):
        file_path = os.path.join(out_path_root, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            pass


def prepare_csv_file(path, columns=None, root_path='out'):
    """Erase each csv file and then add column header row.

    :param path: The path to the CSV file
    :param columns: The columns that define the structure of the file (optional)
    :param root_path: The folder root for output file (optional, defaults to out/)
    """
    # By opening the file for writing, we implicitly delete the file contents
    with open(root_path + '/' + path, 'w') as csv_file:
        # Treat file as CSV
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # Write the header
        if columns is not None:
            csv_writer.writerow([c['name'] for c in columns])


def write_records_to_file(path, columns, entities, entity_filter=None, tbl_name=None, root_path='out'):
    """For a list of entity objects, write a record to an output path. This requires that the objects in the entities
    parameter have a 'get_object_set' method that returns a dictionary of objects whose attributes are available.

    :param path: The path to the CSV file
    :param columns: The dictionary of columns for data values to write for each entity
    :param entities: A list of entity objects to write out to the file
    :param entity_filter: An (attribute, value) tuple that will be evaluated against each object in entities to see if
                          that object should be written to the file. If not provided, all entities are written to file.
                          The attribute is expected to be directly on the entity and is not checked (will raise an
                          exception if not present).
    :param tbl_name: Name of table this row is being generated for (optional). This is used to generate unique record
                     ID values that are unique within a given table.
    :param root_path: The folder root for output file (optional, defaults to out/)
    """
    with open(root_path + '/' + path, 'a') as csv_file:
        # Treat file as CSV
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # Write each row
        for entity in entities:
            if entity_filter is None or getattr(entity, entity_filter[0]) == entity_filter[1]:
                row = writers_util.build_csv_row_values(entity.get_object_set(), columns, available_filters, tbl_name)
                csv_writer.writerow(row)
