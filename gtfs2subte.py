#!/usr/bin/env python

import os
import sys
import libsubte

def main(in_f, out_f):
    print >> sys.stderr, 'Importing GTFS from', in_f
    libsubte.Database.import_gtfs(in_f)

    db = libsubte.Database()
    db.save_as(out_f)
    print >> sys.stderr, 'Saved subte file to', out_f

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage: %s gtfs_directory/ output.subte' % sys.argv[0]
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
