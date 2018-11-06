# nordif2hdf5

Write diffraction patterns in the NORDIF DAT-file to an HDF5-file. To scripts are provided.

### nordif2hdf5.py

This script uses HyperSpy, a multidimensional data analysis library in Python with loads of useful and powerful methods for processing and analysing multidimensional datasets. Running it:

  * Install necessary libraries ([HyperSpy](https://github.com/hyperspy/hyperspy/) and [NumPy](http://www.numpy.org/)) into your [Conda](https://www.anaconda.com/download/) environment or virtualenv.
  * Change file path and name and grid dimension and pattern size in file
  * Run file

### nordif2hdf5.m

This script just uses Matlab. Running it:

```matlab
[settings,patterns] = nordif2hdf5('/home/hakon/kode/nordif_astroebsd/datasett3/Pattern.dat');
```
