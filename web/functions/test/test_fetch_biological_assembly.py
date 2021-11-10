import main as server
import os
import unittest
from unittest.mock import Mock


class TestFetchBiologicalAssembly(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        self.rotated_pdbfile.close()
        return super().tearDown()

    def test_post_pdb_code(self):
        pdb_code = "5V8K"
        data = {"pdb_code": pdb_code}
        request = Mock(get_json=Mock(return_value=data))
