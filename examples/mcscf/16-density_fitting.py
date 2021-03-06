#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

from pyscf import gto, scf, mcscf

'''
Density fitting for orbital optimzation.

NOTE mcscf.density_fit function decorates the mcscf.CASSCF object to
approximate the second order optimization solver.  There is no approximation
for the 2e integrals.  They are evaluated by the regular 4-center integration.
To approximate every 2e integrals using density fitting method,  we need
decorate the SCF object with density_fit function.  (The "overall" density
fitting is new in PySCF-1.1).

This rule basically follows the same convention used in the SCF decoration.
See pyscf/mcscf/df.py for more details and
pyscf/example/scf/23-decorate_scf.py as an exmple
'''

mol = gto.Mole()
mol.build(
    atom = [
    ["C", (-0.65830719,  0.61123287, -0.00800148)],
    ["C", ( 0.73685281,  0.61123287, -0.00800148)],
    ["C", ( 1.43439081,  1.81898387, -0.00800148)],
    ["C", ( 0.73673681,  3.02749287, -0.00920048)],
    ["C", (-0.65808819,  3.02741487, -0.00967948)],
    ["C", (-1.35568919,  1.81920887, -0.00868348)],
    ["H", (-1.20806619, -0.34108413, -0.00755148)],
    ["H", ( 1.28636081, -0.34128013, -0.00668648)],
    ["H", ( 2.53407081,  1.81906387, -0.00736748)],
    ["H", ( 1.28693681,  3.97963587, -0.00925948)],
    ["H", (-1.20821019,  3.97969587, -0.01063248)],
    ["H", (-2.45529319,  1.81939187, -0.00886348)],],
    basis = 'ccpvtz'
)

mf = scf.RHF(mol)
mf.conv_tol = 1e-8
e = mf.kernel()

mc = mcscf.density_fit(mcscf.CASSCF(mf, 6, 6))
mo = mc.sort_mo([17,20,21,22,23,30])
mc.kernel(mo)
print('E(CAS) = %.12f, ref = -230.848493421389' % mc.e_tot)

