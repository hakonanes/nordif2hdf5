# -*- coding: utf-8 -*-
"""
Convert NORDIF DAT-file with Kikuchi diffraction patterns to HyperSpy HDF5
format.

Assumes you can have your full dataset in memory! Will look at a smarter
solution in the future.

Created by Håkon W. Ånes (hakon.w.anes@ntnu.no)
2018-10-30
"""

import hyperspy.api as hs
import numpy as np


# Set file path and file name
datadir = '/home/hakon/kode/nordif_astroebsd/datasett/'
fname = 'Pattern'

# Set grid dimensions and pattern size (in px). Will take this from
# Settings.txt in the near future with regular expressions
scanx = 20
scany = 20
dp_width = 120 # Acquisition px
dp_height = 120

dp_size = dp_width * dp_height  # 1 byte per pixel
dat_size = scanx * scany * dp_size

dat = np.zeros((scany, scanx, dp_height, dp_width), dtype='uint8')

with open(datadir + fname + '.dat', mode='rb') as f:
    f.seek(-dat_size, 2)  # 2: from end of file
    for y in range(scany):
        for x in range(scanx):
            img = f.read(dp_size)
            img = np.fromstring(img, dtype='uint8')  # creates 1-D array
            img.shape = (dp_height, dp_width)  # make 2-D array
            dat[y, x, :, :] = img

s = hs.signals.Signal2D(dat)

s.save(datadir + fname + '.hdf5')
