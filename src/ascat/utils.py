# Copyright (c) 2021, TU Wien, Department of Geodesy and Geoinformation
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of TU Wien, Department of Geodesy and Geoinformation
#      nor the names of its contributors may be used to endorse or promote
#      products derived from this software without specific prior written
#      permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL TU WIEN DEPARTMENT OF GEODESY AND
# GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from gzip import GzipFile
from tempfile import NamedTemporaryFile

import numpy as np
import xarray as xr


def tmp_unzip(filename):
    """
    Unzip file to temporary directory.

    Parameters
    ----------
    filename : str
        Filename.

    Returns
    -------
    unzipped_filename : str
        Unzipped filename
    """
    with NamedTemporaryFile(delete=False) as tmp_fid:
        with GzipFile(filename) as gz_fid:
            tmp_fid.write(gz_fid.read())
        unzipped_filename = tmp_fid.name

    return unzipped_filename


def get_toi_subset(ds, toi):
    """
    Filter dataset for given time of interest.

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset to be filtered for time of interest.
    toi : tuple of datetime
        Time of interest.

    Returns
    -------
    ds : xarray.Dataset
        Filtered dataset.
    """
    if isinstance(ds, dict):
        for key in ds.keys():
            subset = ((ds[key]['time'] > np.datetime64(toi[0])) &
                      (ds[key]['time'] < np.datetime64(toi[1])))
            if isinstance(ds, xr.Dataset):
                ds[key] = ds[key].sel(obs=np.nonzero(subset.values)[0])
            elif isinstance(ds, np.ndarray):
                ds[key] = ds[key][subset]
    else:
        subset = ((ds['time'] > np.datetime64(toi[0])) &
                  (ds['time'] < np.datetime64(toi[1])))
        if isinstance(ds, xr.Dataset):
            ds = ds.sel(obs=np.nonzero(subset.values)[0])
        elif isinstance(ds, np.ndarray):
            ds = ds[subset]

    return ds


def get_roi_subset(ds, roi):
    """
    Filter dataset for given region of interest.

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset to be filtered for region of interest.
    roi : tuple of 4 float
        Region of interest: latmin, lonmin, latmax, lonmax

    Returns
    -------
    ds : xarray.Dataset
        Filtered dataset.
    """
    if isinstance(ds, dict):
        for key in ds.keys():
            subset = ((ds[key]['lat'] > roi[0]) & (ds[key]['lat'] < roi[2]) &
                      (ds[key]['lon'] > roi[1]) & (ds[key]['lon'] < roi[3]))
            if isinstance(ds, xr.Dataset):
                ds[key] = ds[key].sel(obs=np.nonzero(subset.values)[0])
            elif isinstance(ds, np.ndarray):
                ds[key] = ds[key][subset]
    else:
        subset = ((ds['lat'] > roi[0]) & (ds['lat'] < roi[2]) &
                  (ds['lon'] > roi[1]) & (ds['lon'] < roi[3]))
        if isinstance(ds, xr.Dataset):
            ds = ds.sel(obs=np.nonzero(subset.values)[0])
        elif isinstance(ds, np.ndarray):
            ds = ds[subset]

    return ds


def dataset_to_array(ds, dim='obs'):
    """
    Convert xarray.Dataset to numpy.array.

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset to be converted.
    dim : str
        Reference dimension.

    Returns
    -------
    arr : numpy.ndarray
        Numpy array.
    """
    dtype = []
    for var in ds.variables:
        if len(ds.variables[var].shape) == 1:
            dtype.append((var, ds.variables[var].dtype.str))
        elif len(ds.variables[var].shape) > 1:
            shape = ds.variables[var].shape[1:]
            dtype.append((var, ds.variables[var].dtype.str, shape))

    arr = np.empty(ds.dims[dim], dtype=np.dtype(dtype))

    for var in ds.variables:
        arr[var] = ds.variables[var].values

    return arr
