# ----------------------------------------------------------------------------
# Copyright (c) 2024, Liz Gehret.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import subprocess
from qiime2 import Metadata
from q2_types.ordination import PCoAResults


def pcoa_2d(output_dir: str, metadata: Metadata,
            ordination: PCoAResults, measure: str = 'Unweighted Unifrac',
            average: bool = False, week_annotations: bool = True,
            invert_x: bool = True, invert_y: bool = True,
            swap_axes: bool = False, himalaya: bool = False,
            pit_toilet: bool = False, highlighted_buckets: str = ''):

    # metadata_fp = os.path.join(output_dir, 'metadata.tsv')
    # ordination_fp = os.path.join(output_dir, 'ordination.txt')

    # metadata.save(metadata_fp)
    # ordination.export_data(ordination_fp)

    ordination_fp = ordination.export_data()

    metadata_fp = metadata.save(filepath='metadata', ext='.tsv')
    raise ValueError(metadata_fp)

    average_str = str(average)
    week_annotations_str = str(week_annotations)
    invert_x_str = str(invert_x)
    invert_y_str = str(invert_y)
    swap_axes_str = str(swap_axes)
    himalaya_str = str(himalaya)
    pit_toilet_str = str(pit_toilet)

    plot_fp = os.path.join(output_dir, 'pcoa_plot.png')

    command = [
        'python', 'scripts/plot_pcoa_2d.py',
        metadata_fp,
        ordination_fp,
        measure,
        average_str,
        week_annotations_str,
        plot_fp,
        invert_x_str,
        invert_y_str,
        swap_axes_str,
        himalaya_str,
        pit_toilet_str,
        highlighted_buckets
    ]

    subprocess.run(command, check=True)

    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>2D {measure} PCoA Plot</title>
        </head>
        <body>
            <h1>2D {measure} PCoA Plot</h1>
            <img src="pcoa_plot.png" alt="PCoA Plot">
        </body>
        </html>
        ''')
