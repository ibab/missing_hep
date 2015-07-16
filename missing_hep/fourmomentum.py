"""
Implementation of a vectorized four-momentum vector class
Adapted from
    http://lapth.cnrs.fr/pg-nomin/wymant/FourMomentumClass.py
originally implemented by Chris Waymant
"""

import numpy as np

class FourMomentum:

  def __init__(self, E, px, py, pz):
    self.E = np.array(E)
    self.px = np.array(px)
    self.py = np.array(py)
    self.pz = np.array(pz)

  def __add__(self, other):
    return FourMomentum(
             self.E + other.E,
             self.px + other.px,
             self.py + other.py,
             self.pz + other.pz
           )

  def __sub__(self, other):
    return FourMomentum(
             self.E - other.E,
             self.px - other.px,
             self.py - other.py,
             self.pz - other.pz
           )

  def __mul__(self, other):
    return self.E * other.E - self.px * other.px - self.py * other.py - self.pz * other.pz

  def mass(self):
    return np.sqrt(self * self)

  def dot3D(self,other):
    return (self.px * other.px + self.py * other.py + self.pz * other.pz)

  def angle(self,other):
    costheta = self.dot3D(other) / (self.dot3D(self) * other.dot3D(other))
    return np.arccos(costheta)

  def phi(self):
    phitemp = np.arctan2(self.py,self.px)
    phitemp[phitemp < 0] += 2 * np.pi
    return phitemp

  def pT(self):
    return (self.px**2 + self.py**2)**0.5

  def p(self):
    return np.sqrt(self.dot3D(self))

  def theta(self):
    return np.arctan2(self.pT(), self.pz)

  def eta(self):
    thetatemp = self.theta()
    return -np.log(np.tan(thetatemp/2.0))

  def deltaPhi(self, other):
    delta_phi = np.abs(self.phi() - other.phi())
    tmp = delta_phi[delta_phi > np.pi]
    tmp = 2 * np.pi - tmp
    return delta_phi

  def deltaR(self, other):
    delta_phi = self.deltaPhi(other)
    delta_eta = np.abs(self.eta()-other.eta())
    return np.sqrt(delta_phi**2 + delta_eta**2)

  def eT(self):
    return np.sqrt((self.px**2 + self.py**2) + self * self)

