#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

from pyscf import gto, scf, mcscf

'''
Tune CASSCF parameters to reduce the FCI solver cost.

The default CASSCF settings are optimized for large system so that the cost of
IO and integral transformation are minimal.  But they are not optimal for
small systems which call expensive FCI solver.  Taking high order expansion for
matrix elements (.ci_update_dep) and more micro iterations (.max_cycle_micro)
can increase the cost of integration but reduce the total time needed FCI solver.

These settings are useful when DMRG-SCF is executed for small systems.
'''

mol = gto.M(atom='''
C   0       0          0
H  .990138, -0.436705  0
H -.990138, -0.436705  0''',
            basis = 'ccpvdz',
            symmetry = 1,
            spin = 2)
mf = scf.RHF(mol)
mf.kernel()

mc = mcscf.CASSCF(mf, 14, 6)
mc.verbose = 4
mc.ci_update_dep = 4
mc.max_cycle_micro = 10
mc.kernel()
