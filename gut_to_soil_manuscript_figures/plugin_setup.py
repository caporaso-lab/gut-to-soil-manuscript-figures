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
    short_description=''
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
        'export_legend': Bool,
        'highlighted_buckets': Str
    },
    input_descriptions={
        'ordination': 'The two-dimensional `PCoAResults` object that should be'
                      ' used to generate the plot.'
    },
    parameter_descriptions={
        'metadata': 'The Metadata associated with the `PCoAResults` input.',
        'measure': 'The measure that the `PCoAResults` input was generated'
                   ' from. Used for plot title and labeling.',
        'average': 'Whether to plot the weekly average for all buckets at each'
                   ' timepoint.',
        'week_annotations': 'Whether to include numeric labels for each'
                            ' week timepoint for any highlighted bucket(s).',
        'invert_x': 'Whether to invert the x-axis (based on PCoA axis 1'
                    ' values). It is recommended to generate the plot once'
                    ' with both axis inversions disabled to examine the'
                    ' default orientation (to determine if this is needed).',
        'invert_y': 'Whether to invert the y-axis (based on PCoA axis 2'
                    ' values). It is recommended to generate the plot once'
                    ' with both axis inversions disabled to examine the'
                    ' default orientation (to determine if this is needed).',
        'swap_axes': 'Whether to swap the x&y axes.'
                    ' It is recommended to generate the plot once'
                    ' with this parameter disabled to examine the'
                    ' default orientation (to determine if this is needed).',
        'himalaya': 'Whether to include data from'
                    ' the external himalaya study.',
        'pit_toilet': 'Whether to include data from'
                      ' the external pit toilet study.',
        'export_legend': 'Whether to hide the legend in the plot and'
                         ' export it as a separate `.png` file within the'
                         ' `data` directory. If disabled, the legend will be'
                         ' present in the plot.',
        'highlighted_buckets': 'The bucket(s) that should be highlighted in'
                               ' the plot. If including multiple buckets,'
                               ' please use the following format: "2, 3, 4".'
    },
    name='',
    description=('')
)
