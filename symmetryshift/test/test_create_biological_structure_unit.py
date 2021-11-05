import unittest, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from symmetryshift.create_biological_structure_unit import (
    operator
)
from Bio.PDB import PDBParser, parse_pdb_header

class TestCore (unittest.TestCase):
    def test_operator(self):
        pdb_code = "1KZU"
        parser = PDBParser(QUIET=True)

        reference_file = "{}/assets/{}.pdb_rotated".format(os.path.dirname(os.path.abspath(__file__)), pdb_code)
        reference_structure = parser.get_structure(pdb_code, reference_file)

        original_file = "{}/assets/{}.pdb_original".format(os.path.dirname(os.path.abspath(__file__)), pdb_code)
        original_structure = parser.get_structure(pdb_code, original_file)
        original_header = parse_pdb_header(original_file)
        created_structure = operator(structure=original_structure, header=original_header)

        assert(reference_structure, created_structure)

class TestCli (unittest.TestCase):
    def test_only_pdb_code(self):
        pass
    def test_from_file(self):
        pass
    def test_from_