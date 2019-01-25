"""
pyrad.prod.process_product
==========================

Functions for obtaining Pyrad products from the datasets

.. autosummary::
    :toctree: generated/

    generate_traj_product

"""

from ..io.io_aux import get_save_dir, make_filename
from ..io.timeseries import TimeSeries
from ..graph.plots_vol import plot_pos


def generate_traj_product(traj, prdcfg):
    """
    Generates trajectory products

    Parameters
    ----------
    traj : Trajectory object

    prdcfg : dictionary of dictionaries
        product configuration dictionary of dictionaries

    Returns
    -------
    None

    """

    dssavedir = prdcfg['dsname']
    if 'dssavename' in prdcfg:
        dssavedir = prdcfg['dssavename']

    if prdcfg['type'] == 'TRAJ_PLOT':

        timeinfo = traj.time_vector[0]

        savedir = get_save_dir(prdcfg['basepath'], prdcfg['procname'],
                               dssavedir, prdcfg['prdname'],
                               timeinfo=timeinfo)

        ts = TimeSeries("", traj.time_vector,
                        timeformat="%Y-%m-%d %H:%M:%S.%f")

        if prdcfg['datatype'] == 'EL':
            fname = make_filename('ts', prdcfg['dstype'], 'TRAJ',
                                  prdcfg['imgformat'],
                                  prdcfginfo="EL", timeinfo=timeinfo,
                                  timeformat='%Y%m%d%H%M%S',
                                  runinfo=prdcfg['runinfo'])

            ts.add_dataseries("Elevation", "Elevation", "deg",
                              traj.radar_list[0].elevation_vec)
            ts.plot(savedir + fname[0])

        elif prdcfg['datatype'] == 'AZ':
            fname = make_filename('ts', prdcfg['dstype'], 'TRAJ',
                                  prdcfg['imgformat'],
                                  prdcfginfo="AZ", timeinfo=timeinfo,
                                  timeformat='%Y%m%d%H%M%S',
                                  runinfo=prdcfg['runinfo'])

            ts.add_dataseries("Azimuth", "Azimuth", "deg", traj.radar_list[0].azimuth_vec)
            ts.plot(savedir + fname[0])

        elif prdcfg['datatype'] == 'RANGE':
            fname = make_filename('ts', prdcfg['dstype'], 'TRAJ',
                                  prdcfg['imgformat'],
                                  prdcfginfo="RANGE", timeinfo=timeinfo,
                                  timeformat='%Y%m%d%H%M%S',
                                  runinfo=prdcfg['runinfo'])

            ts.add_dataseries("Range", "Range", "m", traj.radar_list[0].range_vec)
            ts.plot(savedir + fname[0])

        else:
            raise Exception("ERROR: Unknown datatype '%s' (dataset: '%s')" %
                            (prdcfg['datatype'], prdcfg['dsname']))

        return None

    elif prdcfg['type'] == 'TRAJ_TEXT':

        timeinfo = traj.time_vector[0]

        savedir = get_save_dir(prdcfg['basepath'], prdcfg['procname'],
                               dssavedir, prdcfg['prdname'],
                               timeinfo=timeinfo)

        fname = make_filename('ts', prdcfg['dstype'], 'TRAJ', ['csv'],
                              prdcfginfo=None, timeinfo=timeinfo,
                              timeformat='%Y%m%d%H%M%S',
                              runinfo=prdcfg['runinfo'])

        description = ["Description:",
                       "Time series of a plane trajectory in radar "
                       "coordinates."]

        ts = TimeSeries(description, traj.time_vector,
                        timeformat="%Y-%m-%d %H:%M:%S.%f")
        ts.add_dataseries("Elevation", "Elevation", "deg",
                          traj.radar_list[0].elevation_vec)
        ts.add_dataseries("Azimuth", "Azimuth", "deg",
                          traj.radar_list[0].azimuth_vec)
        ts.add_dataseries("Range", "Range", "m", traj.radar_list[0].range_vec)

        ts.add_dataseries("Absolute Speed", "Absolute Speed", "m/s",
                          traj.radar_list[0].v_abs)
        ts.add_dataseries("Radial Speed", "Radial Speed", "m/s",
                          traj.radar_list[0].v_r)
        ts.add_dataseries("Elevation Speed", "Elevation Speed", "deg/s",
                          traj.radar_list[0].v_el)
        ts.add_dataseries("Azimuth Speed", "Azimuth Speed", "deg/s",
                          traj.radar_list[0].v_az)

        ts.write(savedir + fname[0])

        return None

    elif prdcfg['type'] == 'TRAJ_MAP': #Trajectory on a map
    
        timeinfo = traj.time_vector[0]

        savedir = get_save_dir(prdcfg['basepath'], prdcfg['procname'],
                               dssavedir, prdcfg['prdname'],
                               timeinfo=timeinfo)

        
        fname = make_filename('ts', prdcfg['dstype'], 'TRAJ',
                                  prdcfg['imgformat'],
                                  prdcfginfo="MAP", timeinfo=timeinfo,
                                  timeformat='%Y%m%d%H%M%S',
                                  runinfo=prdcfg['runinfo'])

        title = "Trajectory Starting at  %s" % \
                traj.time_vector[0].strftime("%Y-%m-%d")

        fname_list=fname
        for i,fname in enumerate(fname_list):
            fname_list[i] = savedir+fname

        # Get traj
        lat=traj.wgs84_lat_deg
        lon=traj.wgs84_lon_deg
        alt=traj.wgs84_alt_m

        fig=plot_pos(
            lat, lon,
            alt,
            fname_list,cb_label='Altitude [m]',
            titl=title,save_fig=True)


    else:
        raise Exception("ERROR: Unsupported product type: '%s' of dataset '%s'"
                        % (prdcfg['type'], prdcfg['dsname']))
