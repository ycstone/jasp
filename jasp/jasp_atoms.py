from ase import Atom, Atoms
import numpy as np
import pickle

def atoms_equal(self, other):
    '''
    check if two atoms objects are identical

    I monkeypatch the ase class because the ase.io read/write
    functions often result in float errors that make atoms not be
    equal. The problem is you may write out 2.0000000, but read in
    1.9999999, which looks different by absolute comparison. I use
    float tolerance for the comparison here.
    '''
    if other is None:
        return False

    TOLERANCE = 1e-6

    a = self.arrays
    b = other.arrays

    # check if number of atoms have changed.
    if len(self)!= len(other):
        return False

    if (a['numbers'] != b['numbers']).all():
        # atom types have changed
        return False

    if (np.abs(a['positions'] - b['positions']) > TOLERANCE).any():
        # something moved
        return False

    if (np.abs(self._cell - other.cell) > TOLERANCE).any():
        # cell has changed
        return False

    # check constraints
    if pickle.dumps(self._constraints) != pickle.dumps(other._constraints):
        return False

    # we do not consider pbc becaue vasp is always periodic
    return True

Atoms.__eq__ = atoms_equal

def set_volume(self, volume, scale_atoms=True):
    '''
    convenience function to set the volume of a unit cell.

    by default the atoms are scaled to the new volume
    '''
    v0 = self.get_volume()
    cell0 = self.get_cell()

    f = (volume/v0)**(1./3.)
    self.set_cell(f*cell0, scale_atoms=scale_atoms)

Atoms.set_volume = set_volume

old_repr = Atoms.__repr__
import textwrap
def new_repr(self):
    '''
    wraps the old __repr__ to return a textwrapped string with fixed width.
    '''
    s = old_repr(self)
    return textwrap.fill(s, width=70, subsequent_indent=' '*6)
Atoms.__repr__ = new_repr

if __name__ == '__main__':
    from ase.data.molecules import molecule

    atoms = molecule('CH3CH2OH')
    print atoms
