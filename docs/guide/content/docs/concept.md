---
weight: 30
---

# Concept of Symmetry shift

## Background

The PDB (Protein Data Bank) file contains the coordinates of all atoms in the unit structure, as shown below. The boxed area shows the x-, y-, and z-coordinates of the atoms, from left to right.

![pdb_coord](https://user-images.githubusercontent.com/84301337/139531746-ee44b003-c757-45d6-8399-9bde1ea79c4c.jpg)

It consists mainly of atom, structure, and chain, and the biopython package makes use of this information.

But it only contains data for the unit structure, so it is not possible to get all the structural data at once.

![pdb_compe_en](https://user-images.githubusercontent.com/84301337/140019178-57cb40cc-1d7a-4f43-be5d-f352f842c8d2.jpg)


Thus, we decided to perform symmetric operations to the coordinates of the atoms, taking advantage of the fact that the PDB file has the information of the original structure as a comment.

![matrix_shift](https://user-images.githubusercontent.com/84301337/139531506-93b5b24b-f1b0-4071-8fee-1d0d63909919.jpg)

This is a set from BIOMT1 to BIOMT3, where the blue boxed area is the rotation matrix and the yellow boxed area is the translation vector.
The green box indicates that the rotation matrix part is a unit matrix and the translation vector part is a zero vector. So, it represents the unit structure itself described in this PDB file.

By applying this rotation matrix and translation vector to the coordinates in the PDB file, we can obtain the coordinates after symmetry operations.

In other words, we assume that the original coordinate of an atom is {{< katex >}}\vec{r}{{< /katex >}}, the rotation matrix is {{< katex >}}A{{< /katex >}}, and the translation vector is {{< katex >}}\vec{b}{{< /katex >}} . The coordinate after symmetry operations {{< katex >}}\vec{r'}{{< /katex >}}
is expressed

{{< katex display >}}
\vec{r'}=A\vec{r}+\vec{b}
{{< /katex >}}

We perform this operation on each atom, for as many symmetric operations as we need.

## Workflow

This product automates this process of rotation and translation for almost all PDB files.

Here is a concrete explanation. The following diagram is the workflow of symmetry shift. The red color indicates the part that we developed or added functions. The yellow-green (greenish) parts are the functions that the Bio.

![Workflow of symmetry shift](workflow.drawio.svg)

The user specifies the PDB ID from which he or she wants to retrieve the biological assembly, either in the CLI or as an argument to the Python package. There is no further input from the user. Everything is done within symmetry shift.

```sh
symmetry 5V8K # PDB ID is 5V8K
```

as a package:

```python
from symmetryshift.create_biological_structure_unit import create, save

pdb_id = "5V8K"
new_structure = create(pdb_id)
save(new_structure)
```

symmetry shift gets a PDB file from a free public data server using `Bio.PDB`(**Recieve PDB ID**)

The next step is to analyze the header (**Get matrix**) and get the coordinates of all atoms (**Get coordinates of Atoms**). Symmetry shift use `PDB.PDBParser` and `PDB.parse_pdb_header`, respectively.

The PDB file contains a header row, where the rotation matrix and translation vector are described in a fixed format.(See Background for details.)

Once we get matrix and vector, Symmetry shift work operators:

```python
new_chain = chain * operator["matrix"] + operator["shift"]
```

Finnaly, Symmetry shift save new PDB file.
