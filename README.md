# nordif2hdf5

Write diffraction patterns in the NORDIF DAT-file to an HDF5-file. Two scripts are provided.

### nordif2hdf5.py

This script uses HyperSpy, a multidimensional data analysis library in Python with loads of useful and powerful methods for processing and analysing multidimensional datasets. Running it:

  * Install necessary libraries in `requirements.txt` ([HyperSpy](https://github.com/hyperspy/hyperspy/) and [NumPy](http://www.numpy.org/)) into your [Conda](https://www.anaconda.com/download/) environment or virtualenv.
  * Change file path and name and grid dimension and pattern size in file
  * Run file

### nordif2hdf5.m

This script just uses Matlab. Running it:

```matlab
[settings,patterns] = nordif2hdf5('/path/to/nordif/directory/Pattern.dat');
```

Check docstring for further details (`help nordif2hdf5`).

### hdf52nordif.py

Write an HDF5 HyperSpy file with electron backscatter diffraction patterns to a binary file readable by TSL-EDAX/NORDIF software.
