"""
The data generator for the SBAC project.

"""

import argparse
import datetime

from datagen.worker_manager import WorkerManager

if __name__ == '__main__':
    # Argument parsing for task-specific arguments
    parser = argparse.ArgumentParser(description='SBAC data generation utility.',
                                     epilog='Example arguments:' +
                                            '\n  --state_type devel --gen_iab --gen_item --xml_out --out_dir out'
                                            '\n  --state_type tiny --gen_sum --xml_out --out_dir out'
                                            '\n  --state_type california --gen_sum --gen_ica --xml_out --out_dir out'
                                     )

    parser.add_argument('-sn', '--state_name', dest='state_name', action='store', default='California', help='The name of the state (default=California)')
    parser.add_argument('-sc', '--state_code', dest='state_code', action='store', default='CA', help='The code of the state to generate data for')
    parser.add_argument('-st', '--state_type', dest='state_type', action='store', default='tiny', help='Specify the type of state to generate data for')

    parser.add_argument('-hier', '--hier_source', dest='hier_source', action='store', default='generate', help='Source of hierarchy, either \'generate\' or a CSV pathname, e.g. ./in/hierarchy.csv')

    group = parser.add_argument_group('packages')
    group.add_argument('-pkg', '--pkg_source', dest='pkg_source', action='store', default='generate', help='Source of assessment packages, either \'generate\' or a glob expression matching files, e.g. ./in/20*.csv')
    group.add_argument('-sum', '--sum_pkg', dest='sum_pkg', action='store_true', default=False, help='Load/generate summative assessment packages')
    group.add_argument('-ica', '--ica_pkg', dest='ica_pkg', action='store_true', default=False, help='Load/generate  interim comprehensive assessment packages')
    group.add_argument('-iab', '--iab_pkg', dest='iab_pkg', action='store_true', default=False, help='Load/generate  interim assessment block packages')

    group = parser.add_argument_group('outcomes')
    group.add_argument('-gsum', '--gen_sum', dest='gen_sum', action='store_true', default=False, help='Generate summative outcomes')
    group.add_argument('-gica', '--gen_ica', dest='gen_ica', action='store_true', default=False, help='Generate ICA outcomes')
    group.add_argument('-giab', '--gen_iab', dest='gen_iab', action='store_true', default=False, help='Generate IAB outcomes')
    group.add_argument('-gitem', '--gen_item', dest='gen_item', action='store_true', default=False, help='Generate item level data')

    parser.add_argument('-o', '--out_dir', dest='out_dir', action='store', default='out', help='Specify the root directory for writing output files to')
    # since there is only a single output format right now, default it to true for convenience
    parser.add_argument('-xo', '--xml_out', dest='xml_out', action='store_true', default=True, help='Output data to (TRT) XML')

    args, unknown = parser.parse_known_args()

    if not (args.xml_out):
        print('Please specify at least one output format')
        print('  --xml_out   Output (TRT) XML')
        exit()

    if args.gen_sum and not args.sum_pkg:
        print('Summative outcomes (--gen_sum) assuming SUM package (specify --sum_pkg to avoid this warning)')
        args.sum_pkg = True

    if args.gen_ica and not args.ica_pkg:
        print('ICA outcomes (--gen_ica) assuming ICA package (specify --ica_pkg to avoid this warning)')
        args.ica_pkg = True

    if args.gen_iab and not args.iab_pkg:
        print('IAB outcomes (--gen_iab) assuming IAB package (specify --iab_pkg to avoid this warning)')
        args.iab_pkg = True

    if not (args.sum_pkg or args.ica_pkg or args.iab_pkg):
        print('No assessment package types selected. Please specify at least one')
        print('  --sum_pkg  Summative assessment package')
        print('  --ica_pkg  Interim comprehensive assessment package')
        print('  --iab_pkg  Interim assessment block package')
        exit()

    worker = WorkerManager(args)

    # Record current (start) time
    tstart = datetime.datetime.now()

    worker.prepare()
    worker.run()
    worker.cleanup()

    # Record now current (end) time
    tend = datetime.datetime.now()

    # Print statistics
    print()
    print('Run began at:  {}'.format(tstart))
    print('Run ended at:  {}'.format(tend))
    print('Run run took:  {}'.format(tend - tstart))
    print()
