# ----------------------------------------------------------------------------
# Copyright (c) 2024, Liz Gehret.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources
import skbio
import subprocess

import qiime2


def pcoa_2d(output_dir: str, metadata: qiime2.Metadata,
            ordination: skbio.OrdinationResults,
            measure: str = 'Unweighted Unifrac',
            average: bool = False, week_annotations: bool = False,
            invert_x: bool = False, invert_y: bool = False,
            swap_axes: bool = False, himalaya: bool = False,
            pit_toilet: bool = False, export_legend: bool = False,
            highlighted_buckets: str = ''):

    md = metadata.to_dataframe()

    metadata_fp = os.path.join(output_dir, 'metadata.tsv')
    ordination_fp = os.path.join(output_dir, 'ordination.txt')

    md.to_csv(metadata_fp, sep='\t', index_label='sample-id')
    ordination.write(ordination_fp)

    script_path = \
        pkg_resources.resource_filename(
            'gut_to_soil_manuscript_figures',
            'scripts/plot_pcoa_2d.py'
        )

    average = str(average)
    week_annotations = str(week_annotations)
    invert_x = str(invert_x)
    invert_y = str(invert_y)
    swap_axes = str(swap_axes)
    himalaya = str(himalaya)
    pit_toilet = str(pit_toilet)
    export_legend = str(export_legend)

    plot_fp = os.path.join(output_dir, 'pcoa_plot.png')


    command = [
        'python', script_path,
        metadata_fp,
        ordination_fp,
        measure,
        average,
        week_annotations,
        plot_fp,
        invert_x,
        invert_y,
        swap_axes,
        himalaya,
        pit_toilet,
        export_legend,
        highlighted_buckets,
        legend_fp
    ]
    subprocess.run(command, check=True)

    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>2D PCoA Plot</title>
        </head>
        <body>
            <h1>2D PCoA Plot</h1>
            <img src="pcoa_plot.png" alt="PCoA Plot">
        ''')
        if export_legend:
            f.write('''
                    <p>
                    <img src="legend.png" alt="PCoA Plot legend">
                    ''')
        f.write('''
        </body>
        </html>
        ''')
