from setuptools import setup, find_packages
with open('requirements.txt') as requirements_file:
      install_requirements = requirements_file.read().splitlines()
setup(
      name="symmetry",
      version="0.0.1",
      description="A small package",
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