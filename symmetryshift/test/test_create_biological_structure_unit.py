import filecmp
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from Bio.PDB import PDBParser, parse_pdb_header

from symmetryshift.cli import cli
from symmetryshift.create_biological_structure_unit import operator


class TestCore(unittest.TestCase):
    def test_operator(self):
        pdb_code = "1KZU"
        parser = PDBParser(QUIET=True)

        reference_file = "{}/assets/{}.pdb_rotated".format(
            os.path.dirname(os.path.abspath(__file__)), pdb_code
        )
        reference_structure = parser.get_structure(pdb_code, reference_file)

        original_file = "{}/assets/{}.pdb_original".format(
            os.path.dirname(os.path.abspath(__file__)), pdb_code
        )
        original_structure = parser.get_structure(pdb_code, original_file)
        original_header = parse_pdb_header(original_file)
        created_structure = operator(
            structure=original_structure, header=original_header
        )

        assert (reference_structure, created_structure)


class TestCli(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = tempfile.mkdtemp()
        self.output_filename = os.path.join(self.tmp_dir, "tmp.pdb")
        self.pdb_code = "1KZU"
        self.rotated_filename = "{}/assets/{}.pdb_rotated".format(
            os.path.dirname(os.path.abspath(__file__)), self.pdb_code
        )
        self.original_filename = "{}/assets/{}.pdb_original".format(
            os.path.dirname(os.path.abspath(__file__)), self.pdb_code
        )
        return super().setUp()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_dir)
        return super().tearDown()

    @patch("builtins.input", return_value="y")
    def test_pdb_code_and_outputfile(self, mock_input):
        cli([self.pdb_code, "--output", self.output_filename])
        self.assertTrue(filecmp.cmp(self.rotated_filename, self.output_filename))

    def test_from_file(self):
        cli(["--from-file", self.original_filename, "--output", self.output_filename])
        self.assertTrue(filecmp.cmp(self.rotated_filename, self.output_filename))
