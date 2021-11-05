from re import S
import click
from symmetryshift.create_biological_structure_unit import creater, save_structure

@click.group(invoke_without_command=True)
@click.option("--output", "-o", default="output.pdb", help="Output file name")
@click.pass_context
def cli(ctx, output):
    if ctx.invoked_subcommand is None:
        # structure = creater(pdb_code)
        # save_structure(structure=structure)
        print("hogehoge", output, ctx.invoked_subcommand)
    print("hogehoge", output, ctx.invoked_subcommand)

@click.command(help="PDB code or PDB file. Add --pdb_file option if you use PDB file")
@click.argument("pdb_code", required=True)
def from_code(pdb_code):
    # structure = creater(pdb_code)
    # save_structure(structure=structure)
    print(pdb_code)

@click.command(help="PDB code or PDB file. Add --pdb_file option if you use PDB file")
@click.argument("pdb_file", required=True, type=click.File("rb"))
def from_file(pdb_file, output):
    # structure = creater(pdb_file)
    # save_structure(structure=structure)
    print(pdb_file, output)

cli.add_command(from_code)
cli.add_command(from_file)

if __name__ == '__main__':
    cli(obj={})