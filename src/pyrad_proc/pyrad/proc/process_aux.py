"""
pyrad.proc.process_aux
=============================

Auxiliary functions. Functions to determine the process type, pass raw data to
the product generation functions, save radar data and extract data at
determined points or regions of interest.

.. autosummary::
    :toctree: generated/

    get_process_type
    process_raw
    process_save_radar
    process_point_measurement

"""

from copy import deepcopy
from warnings import warn

import numpy as np

import pyart

from ..io.io_aux import get_datatype_fields, get_fieldname_pyart

from netCDF4 import num2date


def get_process_type(dataset_type):
    """
    maps the dataset type into its processing function and data set format

    Parameters
    ----------
    dataset_type : str
        data set type, i.e. 'RAW', 'SAN', etc.

    Returns
    -------
    func_name : str
        pyrad function used to process the data set type

    dsformat : str
        data set format, i.e.: 'VOL', etc.

    """

    dsformat = 'VOL'
    if dataset_type == 'RAW':
        func_name = 'process_raw'
    elif dataset_type == 'NCVOL':
        func_name = 'process_save_radar'
    elif dataset_type == 'PWR':
        func_name = 'process_signal_power'
    elif dataset_type == 'SNR':
        func_name = 'process_snr'
    elif dataset_type == 'RHOHV_CORRECTION':
        func_name = 'process_correct_noise_rhohv'
    elif dataset_type == 'BIAS_CORRECTION':
        func_name = 'process_correct_bias'
    elif dataset_type == 'L':
        func_name = 'process_l'
    elif dataset_type == 'CDR':
        func_name = 'process_cdr'
    elif dataset_type == 'SAN':
        func_name = 'process_echo_id'
    elif dataset_type == 'ECHO_FILTER':
        func_name = 'process_echo_filter'
    elif dataset_type == 'SNR_FILTER':
        func_name = 'process_filter_snr'
    elif dataset_type == 'VIS_FILTER':
        func_name = 'process_filter_visibility'
    elif dataset_type == 'PHIDP0_ESTIMATE':
        func_name = 'process_estimate_phidp0'
    elif dataset_type == 'PHIDP0_CORRECTION':
        func_name = 'process_correct_phidp0'
    elif dataset_type == 'PHIDP_SMOOTH_1W':
        func_name = 'process_smooth_phidp_single_window'
    elif dataset_type == 'PHIDP_SMOOTH_2W':
        func_name = 'process_smooth_phidp_double_window'
    elif dataset_type == 'PHIDP_KDP_MAESAKA':
        func_name = 'process_phidp_kdp_Maesaka'
    elif dataset_type == 'PHIDP_KDP_LP':
        func_name = 'process_phidp_kdp_lp'
    elif dataset_type == 'KDP_LEASTSQUARE_1W':
        func_name = 'process_kdp_leastsquare_single_window'
    elif dataset_type == 'KDP_LEASTSQUARE_2W':
        func_name = 'process_kdp_leastsquare_double_window'
    elif dataset_type == 'ATTENUATION':
        func_name = 'process_attenuation'
    elif dataset_type == 'RAINRATE':
        func_name = 'process_rainrate'
    elif dataset_type == 'HYDROCLASS':
        func_name = 'process_hydroclass'
    elif dataset_type == 'SELFCONSISTENCY_KDP_PHIDP':
        func_name = 'process_selfconsistency_kdp_phidp'
    elif dataset_type == 'SELFCONSISTENCY_BIAS':
        func_name = 'process_selfconsistency_bias'
    elif dataset_type == 'RHOHV_RAIN':
        func_name = 'process_rhohv_rain'
    elif dataset_type == 'ZDR_RAIN':
        func_name = 'process_zdr_rain'
    elif dataset_type == 'MONITORING_RHOHV':
        func_name = 'process_monitoring_rhohv'
    elif dataset_type == 'MONITORING_ZDR':
        func_name = 'process_monitoring_zdr'
    elif dataset_type == 'SUN_HITS':
        func_name = 'process_sun_hits'
        dsformat = 'SUN_HITS'
    elif dataset_type == 'POINT_MEASUREMENT':
        func_name = 'process_point_measurement'
        dsformat = 'TIMESERIES'
    else:
        raise ValueError('ERROR: Unknown dataset type '+dataset_type)

    return func_name, dsformat


def process_raw(procstatus, dscfg, radar=None):
    """
    dummy function that returns the initial input data set

    Parameters
    ----------
    procstatus : int
        Processing status: 0 initializing, 1 processing volume,
        2 post-processing

    dscfg : dictionary of dictionaries
        data set configuration

    radar : Radar
        Optional. Radar object

    Returns
    -------
    new_dataset : Radar
        radar object

    """

    if procstatus != 1:
        return None

    new_dataset = deepcopy(radar)
    return new_dataset


def process_save_radar(procstatus, dscfg, radar=None):
    """
    dummy function that allows to save the entire radar object

    Parameters
    ----------
    procstatus : int
        Processing status: 0 initializing, 1 processing volume,
        2 post-processing

    dscfg : dictionary of dictionaries
        data set configuration

    radar : Radar
        Optional. Radar object

    Returns
    -------
    new_dataset : Radar
        radar object

    """

    if procstatus != 1:
        return None

    new_dataset = deepcopy(radar)
    return new_dataset


def process_point_measurement(procstatus, dscfg, radar=None):
    """
    Obtains the radar data at a point measurement

    Parameters
    ----------
    procstatus : int
        Processing status: 0 initializing, 1 processing volume,
        2 post-processing

    dscfg : dictionary of dictionaries
        data set configuration. Accepted Configuration Keywords::

        datatype : string. Dataset keyword
            The data type where we want to extract the point measurement
        latlon : boolean. Dataset keyword
            if True position is obtained from latitude, longitude information,
            otherwise position is obtained from antenna coordinates
            (range, azimuth, elevation).
        truealt : boolean. Dataset keyword
            if True the user input altitude is used to determine the point of
            interest.
            if False use the altitude at a given radar elevation ele over the
            point of interest.
        lon : float. Dataset keyword
            the longitude [deg]. Use when latlon is True.
        lat : float. Dataset keyword
            the latitude [deg]. Use when latlon is True.
        alt : float. Dataset keyword
            altitude [m MSL]. Use when latlon is True.
        ele : float. Dataset keyword
            radar elevation [deg]. Use when latlon is False or when latlon is
            True and truealt is False
        azi : float. Dataset keyword
            radar azimuth [deg]. Use when latlon is False
        rng : float. Dataset keyword
            range from radar [m]. Use when latlon is False
        AziTol : float. Dataset keyword
            azimuthal tolerance to determine which radar azimuth to use [deg]
        EleTol : float. Dataset keyword
            elevation tolerance to determine which radar elevation to use [deg]
        RngTol : float. Dataset keyword
            range tolerance to determine which radar bin to use [m]

    radar : Radar
        Optional. Radar object

    Returns
    -------
    new_dataset : dict
        dictionary containing the data and metadata of the point of interest

    """
    if procstatus != 1:
        return None

    datagroup, datatype, dataset, product = get_datatype_fields(
            dscfg['datatype'][0])
    field_name = get_fieldname_pyart(datatype)

    if field_name not in radar.fields:
        warn('Unable to extract point measurement information. ' +
             'Field not available')
        return None

    projparams = dict()
    projparams.update({'proj': 'pyart_aeqd'})
    projparams.update({'lon_0': radar.longitude['data']})
    projparams.update({'lat_0': radar.latitude['data']})

    if dscfg['latlon']:
        lon = dscfg['lon']
        lat = dscfg['lat']
        alt = dscfg['alt']
        x, y = pyart.core.geographic_to_cartesian(lon, lat, projparams)

        if not dscfg['truealt']:
            ke = 4./3.  # constant for effective radius
            a = 6378100.  # earth radius
            re = a * ke  # effective radius

            elrad = dscfg['ele'] * np.pi / 180.
            r_ground = np.sqrt(x ** 2. + y ** 2.)
            r = r_ground / np.cos(elrad)
            alt_radar = radar.altitude['data']+np.sqrt(
                r ** 2. + re ** 2. + 2. * r * re * np.sin(elrad)) - re
            alt_radar = alt_radar[0]
        else:
            alt_radar = dscfg['alt']

        r, az, el = pyart.core.cartesian_to_antenna(
            x, y, alt_radar-radar.altitude['data'])
        r = r[0]
        az = az[0]
        el = el[0]
    else:
        r = dscfg['rng']
        az = dscfg['azi']
        el = dscfg['ele']

        x, y, alt = antenna_to_cartesian(r, az, el)
        lon, lat = cartesian_to_geographic(x, y, projparams)

    d_az = np.min(np.abs(radar.azimuth['data'] - az))
    if d_az > dscfg['AziTol']:
        warn(' No radar bin found for point (az, el, r):(' +
             str(az)+', '+str(el)+', '+str(r) +
             '). Minimum distance to radar azimuth '+str(d_az) +
             ' larger than tolerance')
        return None

    d_el = np.min(np.abs(radar.elevation['data'] - el))
    if d_el > dscfg['EleTol']:
        warn(' No radar bin found for point (az, el, r):(' +
             str(az)+', '+str(el)+', '+str(r) +
             '). Minimum distance to radar elevation '+str(d_el) +
             ' larger than tolerance')
        return None

    d_r = np.min(np.abs(radar.range['data'] - r))
    if d_r > dscfg['RngTol']:
        warn(' No radar bin found for point (az, el, r):(' +
             str(az)+', '+str(el)+', '+str(r) +
             '). Minimum distance to radar range bin '+str(d_r) +
             ' larger than tolerance')
        return None

    ind_ray = np.argmin(np.abs(radar.azimuth['data'] - az) +
                        np.abs(radar.elevation['data'] - el))
    ind_r = np.argmin(np.abs(radar.range['data'] - r))

    val = radar.fields[field_name]['data'].data[ind_ray, ind_r]
    time = num2date(radar.time['data'][ind_ray], radar.time['units'],
                    radar.time['calendar'])

    # prepare for exit
    new_dataset = dict()
    new_dataset.update({'value': val})
    new_dataset.update({'datatype': datatype})
    new_dataset.update({'time': time})
    new_dataset.update(
        {'point_coordinates_WGS84_lon_lat_alt': [lon, lat, alt]})
    new_dataset.update({'antenna_coordinates_az_el_r': [az, el, r]})
    new_dataset.update(
        {'used_antenna_coordinates_az_el_r': [radar.azimuth['data'][ind_ray],
         radar.elevation['data'][ind_ray],
         radar.range['data'][ind_r]]})

    return new_dataset
