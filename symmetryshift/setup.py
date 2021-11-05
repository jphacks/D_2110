from setuptools import setup, find_packages
import versioneer

def get_long_description():
      return ""

setup(
      name="symmetryshift",
      version=versioneer.get_version(),
      author="flat35hd99",
      url="https://jphacks.github.io/D_2110/docs/home/",
      cmdclass=versioneer.get_cmdclass(),
      description="Create biological strucre unit from single PDB file",
      long_description=get_long_description(),
      download_url="https://github.com/jphacks/D_2110/",
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