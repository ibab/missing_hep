
from missing_hep import FourMomentum


def test_methods():
    import numpy as np
    E = np.array([10, 20, 30])
    px = np.array([1, 2, 3])
    py = np.array([1, 2, 3])
    pz = np.array([1, 2, 3])

    P = FourMomentum(E, px, py, pz)

    P + P
    P * P
    42 * P
    P * 42
    P.mass()
    P.dot3D(P)
    P.angle(P)
    P.phi()
    P.pT()
    P.p()
    P.theta()
    P.eta()
    P.deltaPhi(P)
    P.deltaR(P)
    P.eT()

