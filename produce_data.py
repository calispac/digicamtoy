#!/usr/bin/env python
from digicamtoy.tracegenerator import NTraceGenerator
import h5py
import numpy as np
from tqdm import trange
import datetime

from commandr import command, Run, SetOptions


@command('main')
def produce_data(
    out_path,
    n_events=100,
    time_start=0,
    time_end=200,
    time_sampling=4,
    n_pixels=1296,
    nsb_rate=0.003,
    crosstalk=0.08,
    gain_nsb=True,
    n_photon=0,
    poisson=True,
    sigma_e=0.8,
    sigma_1=0.8,
    gain=5.8,
    baseline=200,
    time_signal=20,
    jitter=0.3,
    sub_binning=0
):
    n_bins = (time_end - time_start) // time_sampling
    _locals = locals()

    hdf5 = h5py.File(out_path, 'w')
    hdf5.attrs.update(_locals)
    hdf5.attrs['date'] = str(datetime.datetime.now())

    adc_count = hdf5.create_dataset(
        'adc_count',
        dtype=np.uint16,
        shape=(n_events, n_pixels, n_bins),
        chunks=(1, n_pixels, n_bins),
        compression='gzip',
    )

    trace_generator = NTraceGenerator(**_locals)
    for count in trange(n_events):
        next(trace_generator)
        adc_count[count] = trace_generator.adc_count

    hdf5.close()


if __name__ == '__main__':
    SetOptions(main='main')
    Run()
