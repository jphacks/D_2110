import os

# and comment out a line below
from Bio.PDB import PDBIO, PDBList, PDBParser, parse_pdb_header
from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model

# If you want to use in jphacks/D_2110 repository,
# refer Quick install guide on README file
# https://github.com/jphacks/D_2110#quick-install-and-use-guide
# or disable comment-out 3 lines below

# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
# from biopython.Bio.PDB import PDBParser, PDBList, PDBIO, parse_pdb_header


def save_structure(structure: Structure, output="out.pdb"):
    """Save structure as PDB file
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
    pdb_file = pdb.retrieve_pdb_file(pdb_code, pdir=pdb_code, file_format="pdb")
    os.rmdir("obsolete")
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
    return operator(structure=structure, header=header, name=pdb_code)


def get_biological_assembly_from_pdb_file(pdb_file):
    structure, header = get_structure_and_header_from_pdb_file(pdb_file=pdb_file)
    return operator(structure=structure, header=header)


def operator(structure=None, header=None, name="symmetry"):
    """Create biological assembly as a structure"""
    new_models = []
    # Work operator
    for constructed_model_number, constructed_model_operator_dict in enumerate(header["symmetry_operators"]):
        new_chain_ids_candicate = [
                *[chr(i) for i in range(65, 91)],  # A to Z
                *[chr(i) for i in range(97, 123)],  # a to z
        ]
        for model_serial_number, model in enumerate(structure.get_models()):
            new_model_id = constructed_model_number + model_serial_number
            new_model = Model(new_model_id)
            chains = list(model.get_chains())
            # Assemble
            for chain in chains:
                if chain.get_id() in constructed_model_operator_dict["chain_ids"]:
                    for operator in constructed_model_operator_dict["operators"]:
                        """
                        Pay attention, please.
                        We can work operators like r' = Ar + b
                        Moreover, this is a chain, not atoms.
                        We can perform like this because
                        we override Chain.__mul__() and Chain.__add__()

                        Both of them perform:
                        1. Copy original chain.
                        2. Work operator to coodinates of all atoms.
                        3. Return new chain.
                        Go /biopython/Bio/PDB/Chain.py if you are interested in this behaviour.

                        Thus, we can write elegant codes like this:
                        """
                        new_chain = chain * operator["matrix"] + operator["shift"]
                        new_chain._id = new_chain_ids_candicate.pop(0)
                        new_model.add(new_chain)
                else:
                    chain._id = new_chain_ids_candicate.pop(0)
                    new_model.add(chain)
            new_models.append(new_model)

    # Create new structure and input all generated models
    new_structure = Structure(name)
    [new_structure.add(model) for model in new_models]
    return new_structure
