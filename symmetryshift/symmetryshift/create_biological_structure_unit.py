import sys
# If you want to use in jphacks/D_2110 repository, refer Quick install guide on README file
# https://github.com/jphacks/D_2110#quick-install-and-use-guide
# or disable comment-out 3 lines below  

# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
# from biopython.Bio.PDB import PDBParser, PDBList, PDBIO, parse_pdb_header

# and comment out a line below
from Bio.PDB import PDBParser, PDBList, PDBIO, parse_pdb_header
from Bio.PDB.Structure import Structure

def save_structure(structure: Structure, output="out.pdb"):
    """ Save structure as PDB file
    :param structure: A protein structure
    :type structure: L{Structure}

    :param output: Output filename or path
    :type output: L{str}
    """
    io = PDBIO()
    io.set_structure(structure)
    io.save(output)

def get_structure_and_header_from_pdb_code(pdb_code: str):
    # Fetch PDB file
    pdb = PDBList()
    pdb_file = pdb.retrieve_pdb_file(pdb_code, file_format="pdb")
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(pdb_code, pdb_file)
    header = parse_pdb_header(pdb_file)
    return structure, header

def get_structure_and_header_from_pdb_file(pdb_file):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("operated", pdb_file)
    header = parse_pdb_header(pdb_file)
    return structure, header

def get_biological_assembly_from_pdb_code(pdb_code):
    structure, header = get_structure_and_header_from_pdb_code(pdb_code=pdb_code)
    return operator(structure=structure, header=header)

def get_biological_assembly_from_pdb_file(pdb_file):
    structure, header = get_structure_and_header_from_pdb_file(pdb_file=pdb_file)
    return operator(structure=structure, header=header)

def operator(structure=None, header=None):
    """ Create biological assembly as a structure
    """
    models = list(structure.get_models())
    model = models[0] # Because single PDB file should contain single model, we get first one. 
    chains = list(structure.get_chains())

    # Work operator
    chain_ids_to_work_symmetry_operator = header["chain_ids_to_work_symmetry_operator"]
    # Because of chain name/id of PDB file must be A~Z and a~z,
    # We can only create biological assembly that consists of less than 26 * 2 = 52 chains
    new_chain_ids_candicate = [
        *[chr(i) for i in range(65,91)], # A to Z
        *[chr(i) for i in range(97,123)], # a to z
    ]
    # Existing ids
    chain_ids = [chain.get_id() for chain in chains]
    # ids can be used for new chain.
    # id must be unique.
    new_chain_ids = list(x for x in new_chain_ids_candicate if x not in chain_ids)

    for chain in chains:
        if chain.get_id() in chain_ids_to_work_symmetry_operator:
            for operator in header["symmetry_operator"]:
                """
                Pay attention, please.
                We can work operators like r' = Ar + b
                Moreover, this is a chain, not atoms.
                We can perform like this because we override Chain.__mul__() and Chain.__add__()

                Both of them perform:
                1. Copy original chain.
                2. Work operator to coodinates of all atoms.
                3. Return new chain.
                Go /biopython/Bio/PDB/Chain.py if you are interested in this behaviour.

                Thus, we can write elegant codes like this.
                """
                new_chain = chain * operator["matrix"] + operator["shift"]
                new_chain._id = new_chain_ids.pop(0)
                model.add(new_chain)

    # Delete models[0] consists of only unit structure(chains).
    structure.detach_child(0)
    # and insert new one.
    structure.add(model)
    return structure
