# ----------------------------------------------------------------------------
# Copyright (c) 2024, Liz Gehret.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Plugin, Metadata, Bool, Str

from q2_types.ordination import PCoAResults

from gut_to_soil_manuscript_figures import __version__
from gut_to_soil_manuscript_figures._methods import pcoa_2d

plugin = Plugin(
    name='gut-to-soil-manuscript-figures',
    version=__version__,
    website='https://github.com/caporaso-lab/gut-to-coil-manuscript-figures/',
    package='gut_to_soil_manuscript_figures',
    description="Plugin that contains methods for figure generation used in"
                " Jeff Meilander's PhD manuscript.",
    short_description='',
    # The plugin-level citation of 'Caporaso-Bolyen-2024' is provided as
    # an example. You can replace this with citations to other references
    # in citations.bib.
    # citations=[citations['Caporaso-Bolyen-2024']]
)

plugin.visualizers.register_function(
    function=pcoa_2d,
    inputs={'ordination': PCoAResults},
    parameters={
        'metadata': Metadata,
        'measure': Str,
        'average': Bool,
        'week_annotations': Bool,
        'invert_x': Bool,
        'invert_y': Bool,
        'swap_axes': Bool,
        'himalaya': Bool,
        'pit_toilet': Bool,
        'highlighted_buckets': Str
    },
    input_descriptions={},
    parameter_descriptions={},
    name='',
    description=('')
)
