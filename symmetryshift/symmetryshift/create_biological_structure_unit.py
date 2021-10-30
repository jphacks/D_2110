import sys
# If you want to use in jphacks/D_2110 repository, refer Quick install guide on README file
# https://github.com/jphacks/D_2110#quick-install-and-use-guide
# or disable comment-out 3 lines below  

# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
# from biopython.Bio.PDB import PDBParser, PDBList, PDBIO, parse_pdb_header

# and comment out a line below
from Bio.PDB import PDBParser, PDBList, PDBIO, parse_pdb_header

def save_structure(structure, output="out.pdb"):
    """ Save structure as PDB file
    :param structure: A protein structure
    :type structure: L{Structure}

    :param output: Output filename or path
    :type output: L{str}
    """
    io = PDBIO()
    io.set_structure(structure)
    io.save(output)

def creater(pdb_id: str):
    """ Create biological assembly as a structure

    :param pdb_id: A PDB ID
    :type pdb_id: L{str}
    """
    # Fetch PDB file
    pdb = PDBList()
    pdb_file = pdb.retrieve_pdb_file(pdb_id, file_format="pdb")
    
    # Get header information
    dictionary = parse_pdb_header(pdb_file)

    # Get structure
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(pdb_id, pdb_file)
    models = list(structure.get_models())
    model = models[0] # Because single PDB file should contain single model, we get first one. 
    chains = list(structure.get_chains())

    # Work operator
    chain_ids_to_work_symmetry_operator = dictionary["chain_ids_to_work_symmetry_operator"]
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
            for operator in dictionary["symmetry_operator"]:
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

def main():
    pdb_id = sys.argv[1]
    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]
        structure = creater(pdb_id=pdb_id)
        save_structure(structure, output=output_filename)
    else:
        structure = creater(pdb_id=pdb_id)
        save_structure(structure)

if __name__ == "__main__":
    main()
