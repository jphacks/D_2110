import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../biopython'))
from Bio.PDB import PDBParser, PDBList, PDBIO, parse_pdb_header
# from Bio.PDB.PDBException import PDBConstructionException
import numpy as np
import math

pdb_code="1KZU"
pdb = PDBList()
pdb_filename = pdb.retrieve_pdb_file(pdb_code, file_format="pdb")
dictionary = parse_pdb_header(pdb_filename)

parser = PDBParser(QUIET=True)
structure = parser.get_structure(pdb_code, pdb_filename)

models = list(structure.get_models())
model = models[0]

chains = list(structure.get_chains())
residues = list(structure.get_residues())
# print([chain.get_parent() for chain in chains])
# print([residue.get_parent() for residue in residues])
chain_ids_should_beworked_operator = dictionary["chain_ids_to_work_symmetry_operator"]

id_candidates = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
chain_ids = [chain.get_id() for chain in chains]
new_chain_ids = list(x for x in id_candidates if x not in chain_ids)

print(chain_ids)
print(new_chain_ids)

for chain in chains:
    if chain.get_id() in chain_ids_should_beworked_operator:
        for operator in dictionary["symmetry_operator"]:
            new_chain = chain * operator["matrix"] + operator["shift"]
            new_chain._id = new_chain_ids.pop(0)
            model.add(new_chain)
# print(chain_ids_should_beworked_operator)
# new_chain = chains[0] * dictionary["symmetry_operator"][0]["matrix"] + dictionary["symmetry_operator"][0]["shift"]
# new_chain._id = "D"
# model.add(new_chain)

structure.detach_child(0)
structure.add(model)
io = PDBIO()
io.set_structure(structure)
io.save("out_1KZU.pdb")
