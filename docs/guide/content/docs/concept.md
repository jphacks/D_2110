---
weight: 30
---

# Concept of Symmetry shift
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

In other words, we assume that the original coordinate of an atom is $\vec{r}$, the rotation matrix is $A$, and the translation vector is $\vec{b}$ . The coordinate after symmetry operations $\vec{r'}$
is expressed

$$\vec{r'}=A\vec{r}+\vec{b}$$

We perform this operation on each atom, for as many symmetric operations as we need.
