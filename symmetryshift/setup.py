from setuptools import setup, find_packages

setup(
      name="symmetryshift",
      version="0.1.0",
      description="Create biological strucre unit from single PDB file",
      author="flat35hd99",
      packages=find_packages(),
      entry_points={
            "console_scripts": [
                  "symmetry=symmetryshift.create_biological_structure_unit:main",
            ]
      },
      classifiers=[
            'Programming Language :: Python :: 3.6',
      ]
)