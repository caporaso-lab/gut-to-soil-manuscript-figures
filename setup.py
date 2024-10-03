# ----------------------------------------------------------------------------
# Copyright (c) 2024, Liz Gehret.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

import versioneer

description = (
    "Plugin template."
)

setup(
    name="gut-to-soil-manuscript-figures",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD-3-Clause",
    packages=find_packages(),
    author="Liz Gehret",
    author_email="elizabeth.gehret@nau.edu",
    description=description,
    url="https://github.com/caporaso-lab/gut-to-coil-manuscript-figures/",
    entry_points={
        "qiime2.plugins": [
            "gut_to_soil_manuscript_figures="
            "gut_to_soil_manuscript_figures"
            ".plugin_setup:plugin"]
    },
    package_data={
        "gut_to_soil_manuscript_figures": ["citations.bib"],
        "gut_to_soil_manuscript_figures.tests": ["data/*"],
    },
    zip_safe=False,
)
