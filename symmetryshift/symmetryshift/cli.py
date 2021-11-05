import argparse
from symmetryshift.create_biological_structure_unit import (
    get_biological_assembly_from_pdb_code,
    get_biological_assembly_from_pdb_file,
    save_structure
    )

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("PDB object", help="PDB code or PDB file path if you set --from-file.")
    parser.add_argument("--from-file", action="store_true", help="Use file instead of PDB code")
    parser.add_argument("--output", help="Output file name", default="output.pdb")

    args = vars(parser.parse_args())
    if args["from_file"]:
        structure = get_biological_assembly_from_pdb_file(args["PDB object"])
    else:
        structure = get_biological_assembly_from_pdb_code(args["PDB object"])

    save_structure(structure=structure, output=args["output"])

if __name__ == "__main__":
    cli()
