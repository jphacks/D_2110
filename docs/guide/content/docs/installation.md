---
weight: 10
---

# Install guide

## Install via pip

Installation needs [distribution of biopython](https://github.com/flat35hd99/biopython) ([original](https://github.com/biopython/biopython)) we modified.

```sh
pip install git+https://github.com/flat35hd99/biopython
pip install symmetryshift
```

## Verify your installation

Check if your installation succeed.

```sh
# Argument is pdb id.
symmetry 1KZU 
```

You will see success and you can find `out.pdb` file and some directories.

```shell
.
├── kz
│   └── pdb1kzu.ent
├── obsolete
└── out.pdb
```

`out.pdb` is a generated biological assembly PDB file and `kz/pdb1kzu.ent` is original PDB file. You can check structure using protein viewer like VMD and PyMOL.

`kz/pdb1kzu.ent` looks like:

![1KZU](/installation/1KZU.png)

and `out.pdb` looks like:

![generated biological assembly of 1KZU](/installation/1KZU_biological_assembly.png)
