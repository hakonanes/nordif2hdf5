# -*- coding: utf-8 -*-
#
# Write an HDF5 HyperSpy file with electron backscatter diffraction patterns
# to a binary file readable by the NORDIF software.
#
# Created by Håkon W. Ånes (hakon.w.anes@ntnu.no)
# 2018-11-28
#

import hyperspy.api as hs
import os
import argparse


# Parse input parameters
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('file', help='Full path of original file')
parser.add_argument('--lazy', dest='lazy', default=False, action='store_true',
                    help='Whether to read/write lazy or not')
arguments = parser.parse_args()

# Set data directory, filename and file extension
datadir, fname = os.path.split(arguments.file)
fname, ext = os.path.splitext(fname)

# Read data from file
print('* Read data from file')
s = hs.load(arguments.file, lazy=arguments.lazy)

# Write data to file
print('* Write data to file')
s.data.flatten().tofile(os.path.join(datadir, fname + '.dat'))
