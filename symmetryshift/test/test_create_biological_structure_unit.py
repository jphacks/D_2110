import unittest, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from symmetryshift.create_biological_structure_unit import creater 
from Bio.PDB import PDBParser

class TestCreater (unittest.TestCase):
    def test_creater(self):
        pdb_code = "1KZU"
        reference_file = "{}/assets/{}.pdb_rotated".format(os.path.dirname(os.path.abspath(__file__)), pdb_code)
        parser = PDBParser(QUIET=True)
        reference_structure = parser.get_structure(pdb_code, reference_file)

        created_structure = creater(pdb_code)

        assert(reference_structure, created_structure)
