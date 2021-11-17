import argparse
import shutil
import sys

from symmetryshift.create_biological_structure_unit import (
    get_biological_assembly_from_pdb_code,
    get_biological_assembly_from_pdb_file,
    save_structure,
)


def cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "PDB object", help="PDB code or PDB file path if you set --from-file."
    )
    parser.add_argument(
        "--from-file", action="store_true", help="Use file instead of PDB code"
    )
    parser.add_argument("--output", help="Output file name", default="output.pdb")

    args = vars(parser.parse_args(args))
    if args["from_file"]:
        structure = get_biological_assembly_from_pdb_file(args["PDB object"])
    else:
        structure = get_biological_assembly_from_pdb_code(args["PDB object"])
        while True:
            y_or_n = input("Do you want to remove the original pdb file ? (y/n)")
            if y_or_n == "y":
                shutil.rmtree(args["PDB object"])
                break
            elif y_or_n == "n":
                break
            else:
                continue

    save_structure(structure=structure, output=args["output"])


def main():
    cli(sys.argv[1:])


if __name__ == "__main__":
    main()
