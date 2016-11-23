"""
The data generator for the SBAC project.

"""

import argparse
import datetime

from worker_manager import WorkerManager

if __name__ == '__main__':
    # Argument parsing for task-specific arguments
    parser = argparse.ArgumentParser(description='SBAC data generation task.')
    # udl overrides other settings
    parser.add_argument('-sn', '--state_name', dest='state_name', action='store', default='California', help='The name of the state (default=California)', required=False)
    parser.add_argument('-sc', '--state_code', dest='state_code', action='store', default='CA', help='The code of the state to generate data for', required=False)
    parser.add_argument('-st', '--state_type', dest='state_type', action='store', default='devel', help='Specify the type of state to generate data for', required=False)
    parser.add_argument('-o', '--out_dir', dest='out_dir', action='store', default='out', help='Specify the root directory for writing output files to', required=False)
    parser.add_argument('-ho', '--host', dest='pg_host', action='store', default='localhost', help='The host for the PostgreSQL server to write data to')
    parser.add_argument('-pa', '--pass', dest='pg_pass', action='store', default='', help='The password for the PostgreSQL server to write data to')
    parser.add_argument('-s', '--schema', dest='pg_schema', action='store', default='dg_data', help='The schema for the PostgreSQL database to write data to')
    parser.add_argument('-po', '--pg_out', dest='pg_out', action='store_true', help='Output data to PostgreSQL database', required=False)
    parser.add_argument('-so', '--star_out', dest='star_out', action='store_true', help='Output data to star schema CSV', required=False)
    parser.add_argument('-lo', '--lz_out', dest='lz_out', action='store_true', help='Output data to landing zone CSV and JSON', required=False)
    parser.add_argument('-io', '--il_out', dest='il_out', action='store_true', help='Output item-level data', required=False)
    parser.add_argument('-gia', '--generate_iabs', dest='generate_iabs', action='store_false', default=True, help='generate interim assessment blocks')
    args, unknown = parser.parse_known_args()

    worker = WorkerManager(args)

    # Validate at least one form of output
    if worker.workers is None:
        print('Please specify at least one output format')
        print('  --pg_out    Output to PostgreSQL')
        print('  --star_out  Output star schema CSV')
        print('  --lz_out    Output landing zone CSV and JSON')
        exit()

    # Record current (start) time
    tstart = datetime.datetime.now()

    worker.run()
    worker.cleanup()

    # Record now current (end) time
    tend = datetime.datetime.now()

    # Print statistics
    print()
    print('Run began at:  %s' % tstart)
    print('Run ended at:  %s' % tend)
    print('Run run took:  %s' % (tend - tstart))
    print()
