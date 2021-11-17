from setuptools import find_packages, setup

import versioneer

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "symmetry=symmetryshift.cli:main",
        ]
    },
)
