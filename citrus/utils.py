import numpy as np

from . import constants as cc


def get_density(x, y, z, density, cutoff):
    r_min = cutoff * cc.AU_SI

    r = np.sqrt(x * x + y * y + z * z)

    if r > r_min:
        r_to_use = r
    else:
        r_to_use = r_min

    density[0] = 1.5e6 * ((r_to_use / (300 * cc.AU_SI)) ** (-1.5)) * 1e6

    return density


def get_temperature(x, y, z, temperature, fT_r):
    """
    fT_r is an array containing temperatures as a function
    of radial distance from the origin.
    """
    r = np.sqrt(x * x + y * y + z * z)

    mask = (r > fT_r[0, :-1]) & (r < fT_r[0, 1:])
    x0 = np.where(mask)[0][0]

    if r < fT_r[0, 0]:
        temperature[0] = fT_r[1, 0]
    elif r > fT_r[0, -1]:
        temperature[0] = fT_r[1, -1]
    else:
        temperature[0] = fT_r[1, x0] + (r - fT_r[0, x0]) * (
            fT_r[1, x0 + 1] - fT_r[1, x0]
        ) / (fT_r[0, x0 + 1] - fT_r[0, x0])

    return temperature


def get_abundance(): ...


def get_doppler(): ...


def get_velocity(x, y, z, velocity, cutoff):
    r_min = cutoff * cc.AU_SI

    r = np.sqrt(x * x + y * y + z * z)

    if r > r_min:
        r_to_use = r
    else:
        r_to_use = r_min

    free_fall_velocity = np.sqrt(2.0 * cc.GRAVITATIONAL_CONST_SI * 1.989e30 / r_to_use)

    velocity[0] = -x * free_fall_velocity / r_to_use
    velocity[1] = -y * free_fall_velocity / r_to_use
    velocity[2] = -z * free_fall_velocity / r_to_use

    return velocity


def calculate_source_fn(dtau: float, taylor_cutoff: float):
    """
    Calculate the source function for a given optical depth and cutoff.

    Parameters
    ----------
    dtau : float
        The optical depth.
    taylor_cutoff : float
        The cutoff for the Taylor expansion.

    Returns
    -------
    remnantSnu : float
        The source function.
    exp_dtau : float
        The exponential of the optical depth.
    """
    if np.abs(dtau) < taylor_cutoff:
        remnant_Snu = 1.0 - dtau * (1.0 - dtau * (1.0 / 3.0)) * (1.0 / 2.0)
        exp_dtau = 1.0 - dtau * remnant_Snu
    else:
        exp_dtau: float = np.exp(-dtau)
        remnant_Snu: float = (1.0 - exp_dtau) / dtau
    return remnant_Snu, exp_dtau


def planck_fn(freq: float, temp: float):
    """
    Calculate the Planck function for a given frequency and temperature.

    Parameters
    ----------
    freq : float
        The frequency.
    temp : float
        The temperature.

    Returns
    -------
    bb : float
        The Planck function.
    """
    bb = 10.0
    if temp < np.finfo(float).eps:
        bb = 0.0
    else:
        wn = freq / 299792458.0
        if 6.62607015e-34 * freq > 100 * 1.380649e-23 * temp:
            bb = (
                2.0
                * 6.62607015e-34
                * wn
                * wn
                * freq
                * np.exp(-6.62607015e-34 * freq / 1.380649e-23 / temp)
            )
        else:
            bb = (
                2.0
                * 6.62607015e-34
                * wn
                * wn
                * freq
                / (np.exp(6.62607015e-34 * freq / 1.380649e-23 / temp) - 1.0)
            )
    return bb


def gauss_line(v: float, one_on_sigma: float):
    """
    Calculate the Gaussian line profile for a given velocity and inverse sigma.

    Parameters
    ----------
    v : float
        The velocity.
    one_on_sigma : float
        The inverse sigma.

    Returns
    -------
    float
        The Gaussian line profile.
    """
    val = v * v * one_on_sigma * one_on_sigma
    return np.exp(-val)
