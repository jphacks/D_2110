import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../biopython'))
from Bio.PDB import PDBParser, PDBList, PDBIO
import numpy as np
import math

pdb_code="5V8K"
pdb = PDBList()
pdb_filename = pdb.retrieve_pdb_file(pdb_code, file_format="pdb")

parser = PDBParser(QUIET=True)
structure = parser.get_structure(pdb_code, pdb_filename)

models = list(structure.get_models())
model = models[0]

chains = list(structure.get_chains())
residues = list(structure.get_residues())
# print([chain.get_parent() for chain in chains])
# print([residue.get_parent() for residue in residues])

new_chain = chains[0]
new_chain._id = "D"
model.add(new_chain)

structure.detach_child(0)
structure.add(model)
io = PDBIO()
io.set_structure(structure)
io.save("out2.pdb")
