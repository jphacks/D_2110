from setuptools import setup, find_packages
import versioneer

setup(
      name="symmetryshift",
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description="Create biological strucre unit from single PDB file",
      author="flat35hd99",
      packages=find_packages(),
      entry_points={
            "console_scripts": [
                  "symmetry=symmetryshift.cli:cli",
            ]
      },
      classifiers=[
            'Programming Language :: Python :: 3.6',
      ]
)