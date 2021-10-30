import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../biopython'))

from Bio.PDB import PDBParser, PDBList, parse_pdb_header

pdb_code="1KZU"
pdb = PDBList()
pdb_filename = pdb.retrieve_pdb_file(pdb_code, file_format="pdb")
dictionary = parse_pdb_header(pdb_filename)

print(dictionary["symmetry_operator"])
