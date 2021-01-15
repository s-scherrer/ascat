# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
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

import numpy as np


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
            subset = ((ds[key].time > np.datetime64(toi[0])) &
                      (ds[key].time < np.datetime64(toi[1])))
            ds[key] = ds[key].sel(obs=np.nonzero(subset.values)[0])
    else:
        subset = ((ds.time > np.datetime64(toi[0])) &
                  (ds.time < np.datetime64(toi[1])))
        ds = ds.sel(obs=np.nonzero(subset.values)[0])

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
            subset = ((ds[key].lat > roi[0]) & (ds[key].lon > roi[2]) &
                      (ds[key].lat < roi[1]) & (ds[key].lon < roi[3]))
            ds[key] = ds[key].sel(obs=np.nonzero(subset.values)[0])
    else:
        subset = ((ds.lat > roi[0]) & (ds.lon > roi[2]) &
                  (ds.lat < roi[1]) & (ds.lon < roi[3]))
        ds = ds.sel(obs=np.nonzero(subset.values)[0])

    return ds
