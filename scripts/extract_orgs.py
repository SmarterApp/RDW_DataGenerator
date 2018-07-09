#!/usr/bin/env python

import fnmatch
import json
import os
import sys

from xml.etree import ElementTree

if __name__ == '__main__':
    def log(*args):
        sys.stdout.write(' '.join(str(arg) for arg in args) + '\n')

    # TODO - parse sys.argv for options
    indir = os.path.abspath('.')
    outfile = 'organizations.json'

    districts = {}
    schools = {}

    # because each district is generated individually, we need to read the file to
    # get previous districts, merge the new ones, then rewrite the file ...
    if os.path.isfile(outfile):
        with open(outfile, 'r') as f:
            org = json.load(f)
            if 'districts' in org: districts = {d['entityId']: d for d in org['districts']}
            if 'institutions' in org: schools = {s['entityId']: s for s in org['institutions']}
        log('Loaded', len(districts), 'districts and', len(schools), 'schools')

    processed = 0
    skipped = 0
    bad = 0
    for root, subs, files in os.walk(indir):
        for file in fnmatch.filter(files, '*.xml'):
            try:
                with open(os.path.join(root, file), 'r') as f:
                    state = None
                    districtId = None
                    districtName = None
                    schoolId = None
                    schoolName = None
                    tree = ElementTree.parse(f)
                    for node in tree.findall('.//ExamineeRelationship'):
                        name = node.attrib.get('name')
                        value = node.attrib.get('value')
                        if name == 'StateAbbreviation': state = value
                        elif name == 'DistrictId': districtId = value
                        elif name == 'DistrictName': districtName = value
                        elif name == 'SchoolId': schoolId = value
                        elif name == 'SchoolName': schoolName = value

                    if state and districtId and districtName and schoolId and schoolName:
                        processed += 1
                        if districtId not in districts:
                            districts[districtId] = {
                                'entityId': districtId,
                                'entityName': districtName,
                                'entityType': 'DISTRICT',
                                'parentEntityId': state
                            }
                        if schoolId not in schools:
                            schools[schoolId] = {
                                'entityId': schoolId,
                                'entityName': schoolName,
                                'entityType': 'INSTITUTION',
                                'parentEntityId': districtId
                            }
                    else:
                        skipped += 1
                        log('File', f.name, 'contains insufficient organization data')
            except:
                bad += 1
                log('File', os.path.join(root, file), 'is bad')

    log('Processed', processed, 'files, skipped', skipped, 'files,', bad, 'bad files')
    log('Writing', len(districts), 'districts and', len(schools), 'schools')

    with open(outfile, 'w') as f:
        json.dump({'districts': list(districts.values()), 'institutions': list(schools.values())}, f, indent=2)
