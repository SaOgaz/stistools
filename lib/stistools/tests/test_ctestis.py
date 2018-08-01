import numpy as np
from ..ctestis import ctestis


def test_single_value_ctestis():
    fluxc, dmagc, dyc = ctestis(182., 5000., 150.,
            stisimage='o4qp9g010_crj.fits')

    assert np.allclose([2536.7133], [fluxc])
    assert np.allclose([-0.015828427], [dmagc])
    assert np.allclose([0.007079903], [dyc])

def test_list_values_ctestis():
    fluxc, dmagc, dyc = ctestis([182., 182.], [5000., 1000.], [150., 150.],
            stisimage='o4qp9g010_crj.fits')

    assert np.allclose([2536.71326136, 509.14102614], [fluxc])
    assert np.allclose([-0.01582843, -0.01967022], [dmagc])
    assert np.allclose([0.0070799, 0.00878668], [dyc])
