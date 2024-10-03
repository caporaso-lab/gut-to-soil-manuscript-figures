# ----------------------------------------------------------------------------
# Copyright (c) 2024, Liz Gehret.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Plugin
from q2_types.feature_table import FeatureTable, Frequency
from gut_to_soil_manuscript_figures import __version__
from gut_to_soil_manuscript_figures._methods import duplicate_table

citations = Citations.load("citations.bib", package="gut_to_soil_manuscript_figures")

plugin = Plugin(
    name="gut-to-soil-manuscript-figures",
    version=__version__,
    website="https://github.com/caporaso-lab/gut-to-coil-manuscript-figures/",
    package="gut_to_soil_manuscript_figures",
    description="Plugin that contains methods for figure generation used in Jeff Meilander's PhD manuscript",
    short_description="Plugin template.",
    # The plugin-level citation of 'Caporaso-Bolyen-2024' is provided as
    # an example. You can replace this with citations to other references
    # in citations.bib.
    citations=[citations['Caporaso-Bolyen-2024']]
)

plugin.methods.register_function(
    function=duplicate_table,
    inputs={'table': FeatureTable[Frequency]},
    parameters={},
    outputs=[('new_table', FeatureTable[Frequency])],
    input_descriptions={'table': 'The feature table to be duplicated.'},
    parameter_descriptions={},
    output_descriptions={'new_table': 'The duplicated feature table.'},
    name='Duplicate table',
    description=("Create a copy of a feature table with a new uuid. "
                 "This is for demonstration purposes only. 🧐"),
    citations=[]
)
