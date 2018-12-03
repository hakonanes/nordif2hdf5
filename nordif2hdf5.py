# -*- coding: utf-8 -*-
#
# Convert NORDIF DAT-file with Kikuchi diffraction patterns to HyperSpy HDF5
# format.

# Created by Håkon W. Ånes (hakon.w.anes@ntnu.no)
# 2018-11-20

import hyperspy.api as hs
import numpy as np
import os
import re
import warnings
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

# Get grid dimensions and pattern size from Setting.txt
settings = open(os.path.join(datadir,'Setting.txt'), 'rb')
for i, line in enumerate(settings):
    # Pattern size
    if i == 47:
        match = re.search(b'Resolution\t(.*)\tpx', line).group(1).split(b'x')
        SX, SY = [int(i) for i in match]
    # Grid dimensions
    if i == 79:
        match = re.search(b'Number of samples\t(.*)\t#',
                          line).group(1).split(b'x')
        NX, NY = [int(i) for i in match]
settings.close()

# Get data size
DAT_SZ = NX * NY * SX * SY

# Open in correct mode
if arguments.lazy:
    patterns = open(arguments.file, 'r+b')
else:
    patterns = open(arguments.file, 'rb')

# Read data from file
if not arguments.lazy:
    patterns.seek(-DAT_SZ, 2)
    data = np.fromfile(patterns, dtype='uint8')
else:
    data = np.memmap(patterns, mode='r')

# Reshape data
try:
    data = data.reshape((NX, NY, SX, SY), order='C').squeeze()
except ValueError:
    warnings.warn('Setting.txt dimensions larger than file size!')

# Create HyperSpy signal
if not arguments.lazy:
    s = hs.signals.Signal2D(data)
else:
    s = hs.signals.Signal2D(data).as_lazy()

# Write signal to file
s.save(os.path.join(datadir, fname + '.hdf5'))