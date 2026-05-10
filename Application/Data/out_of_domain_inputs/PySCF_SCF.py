# PySCF Calculation parameters

mol = pyscf.M(atom = '', basis = '')
mol.charge = -1
mol.spin = 1
mol.build()

mf =pyscf.scf.UHF(mol)
mf.init_guess = 'hcore'
mf.max_cycle = 2000
mf.diis_space = 10
mf.conv_tol = 9e-10
mf.conv_tol_grad = 3e-5