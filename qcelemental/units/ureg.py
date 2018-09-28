"""
A wrapper for the pint ureg data
"""

import pint
import os

from ..data import nist_2014_codata
phys_const = nist_2014_codata["constants"]

# We only want the ureg exposed
__all__ = ["ureg", "Quantity"]

ureg = pint.UnitRegistry()
Quantity = ureg.Quantity

# Explicitly update relevant 2014 codata

# Definitions
ureg.define("avogadro_constant = {} / mol = N_A".format(phys_const["avogadro constant"]["value"]))
ureg.define("boltzmann_constant = {} * joule / kelvin".format(phys_const["boltzmann constant"]["value"]))
ureg.define("speed_of_light = {} * meter / second".format(phys_const["speed of light in vacuum"]["value"]))
ureg.define("hartree_inverse_meter = {} / hartree / m".format(phys_const["hartree-inverse meter relationship"]["value"]))

# Energy
ureg.define("hartree = {} * joule = E_h = hartree_energy".format(phys_const["hartree energy"]["value"]))
ureg.define("electron_volt = {} * J = eV".format(phys_const["electron volt-joule relationship"]["value"]))

# Constants
ureg.define("electron_mass = {} * kg".format(phys_const["electron mass"]["value"]))
ureg.define("elementary_charge = {} * coulomb = e".format(phys_const["elementary charge"]["value"]))
ureg.define("plancks_constant = {} * joule * s".format(phys_const["planck constant"]["value"]))

# Distance
ureg.define("bohr = {} * meter = bohr_radius".format(phys_const["bohr radius"]["value"]))
ureg.define("wavenumber = 1 / centimeter")

# Masses
ureg.define(
    "atomic_mass_unit = {} * kilogram = u = amu = dalton = Da".format(phys_const["atomic mass constant"]["value"]))

# Add contexts
c1 = pint.Context("quantum_chemistry")

# Allows hartree <-> frequency
c1 = pint.Context("energy_frequency")
c1.add_transformation("[energy]", "[frequency]", lambda ureg, val: val / ureg.plancks_constant)
c1.add_transformation("[frequency]", "[energy]", lambda ureg, val: val * ureg.plancks_constant)

# Allows hartree <-> length
c2 = pint.Context("energy_length")
c2.add_transformation("[energy]", "1 / [length]", lambda ureg, val: val * ureg.hartree_inverse_meter)
c2.add_transformation("1 / [length]", "[energy]", lambda ureg, val: val / ureg.hartree_inverse_meter)

# Allows energy <-> energy / mol
c3 = pint.Context("substance_relation")
c3.add_transformation("[energy]", "[energy] / [substance]", lambda ureg, val: val * ureg.N_A)
c3.add_transformation("[energy] / [substance]", "[energy]", lambda ureg, val: val / ureg.N_A)

# Add the context
ureg.enable_contexts(c1, c2, c3)
