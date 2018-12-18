# -*- coding: utf-8 -*-
#
# Update NORDIF's Setting.txt with correct, new ROI after cropping a dataset
# in HyperSpy.
#
# Created by Håkon W. Ånes (hakon.w.anes@ntnu.no)
# 2018-11-29
#

import os
import re
import argparse
import tempfile as tf
import shutil as sh


# Parse input parameters
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('file', help='Full path of original Setting.txt file')
parser.add_argument('upper_leftx', help='Upper left x pixel coordinate')
parser.add_argument('upper_lefty', help='Upper left y pixel coordinate')
parser.add_argument('width', help='Width of cropped dataset')
parser.add_argument('height', help='Height of cropped dataset')
args = parser.parse_args()

# Set data directory, filename and file extension
datadir, fname = os.path.split(args.file)
fname, ext = os.path.splitext(fname)

upper_lefty = int(args.upper_lefty)
upper_leftx = int(args.upper_leftx)
width = int(args.width)
height = int(args.height)


def replace_line(line_old, line_num, px, step=None):
    """Replace values in line"""
    # Get values in string
    values = re.findall(b'\d+.?\d+', line_old)

    # Byte string to numbers
    um_old = int(float(values[0].decode('utf8')))
    px_old = int(values[1].decode('utf8'))
    px_size = px_old/um_old

    if line_num == 74 or line_num == 75:  # Top (x) and left (y) coordinate
        um_new = um_old + px/px_size
        px_new = px_old + px
    else:  # Width and height
        um_new = px * step
        px_new = um_new * px_size

    return um_new, px_new


# Create new settings file
fh, abs_path = tf.mkstemp(dir=datadir)

with os.fdopen(fh, 'wb') as file_new:
    with open(args.file, 'rb') as file_old:
        for i, line in enumerate(file_old):  # First get step size in um
            if i == 78:
                step_string = re.findall(b'\d+.?\d+', line)
                step = float(step_string[0].decode('utf8'))
        file_old.seek(0)  # Set files current position to start of file
        for i, line in enumerate(file_old):  # Loop over old file
            # Replace relevant lines
            if i == 74:  # Top (y) coordinate
                y_um, y_px = replace_line(line, i, upper_lefty)
                line = b'Top\t%.3f (%i)\t\xb5m (px)\r\n' % (y_um, y_px)
            if i == 75:  # Left (x) coordinate
                x_um, x_px = replace_line(line, i, upper_leftx)
                line = b'Left\t%.3f (%i)\t\xb5m (px)\r\n' % (x_um, x_px)
            if i == 76:  # Width
                w_um, w_px = replace_line(line, i, width, step)
                line = b'Width\t%.3f (%i)\t\xb5m (px)\r\n' % (w_um, w_px)
            if i == 77:  # Height
                h_um, h_px = replace_line(line, i, height, step)
                line = b'Height\t%.3f (%i)\t\xb5m (px)\r\n' % (h_um, h_px)
            if i == 79:  # Number of samples
                line = b'Number of samples\t%ix%i\t#\r\n' % (height, width)
            file_new.write(line)

# Rename temporary file
sh.move(abs_path, os.path.join(datadir, fname + '_new' + ext))