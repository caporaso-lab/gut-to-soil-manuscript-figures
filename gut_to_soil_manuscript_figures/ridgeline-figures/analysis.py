import json
import os
from pathlib import Path
import sys
from typing import Dict, List

import pandas as pd


def calculate_distances(
    md_fp: str,
    matrix_fp: str,
    bucket_id: int,
    n: int,
    from_beginning: bool = False,
    pre_or_post_roll: str = 'post',
    compare_only_own_fecal: bool = False,
    sep: str = '\t'
) -> Dict[str, List[float]]:
    '''
    Parameters
    ----------
    md_fp : str
        Filepath to the metadata file.
    matrix_fp : str
        Filepath to the distance matrix file.
    bucket_id : int
        The bucket id to use for this comparison.
    n : int
        The number of time points to use beginning with the chronologically
        last time point and moving backwards.
    from_beginning : bool
        Wether to select the `n` time points from the beginning or the end
        of the chronologically sorted time points. End (False) by default.
        Set to True for beginning.
    pre_or_post_roll : str
        Whether to use 'pre-roll' or 'post-roll' composting samples. Post-roll
        by default.
    compare_only_own_fecal : bool
        Whether to make comparisons to only a bucket's own fecal samples. False
        by default.
    sep : str
        The separator to use when parsing the metadata. The distance matrix
        is assumed to be in .tsv format.

    Returns
    -------
    dict of str -> list of float
        A dictionary of sample type comparison to an array of the selected
        distances. Each array is equal in length to `n` times the number of
        values of for that comparison.
    '''
    # validate inputs
    if pre_or_post_roll == 'post':
        bucket_sample_type = 'Human Excrement Compost'
    elif pre_or_post_roll == 'pre':
        bucket_sample_type = 'Human Excrement Compost Pre-Roll'
    else:
        raise ValueError('Use one of pre/post for pre_or_post_roll')

    # md wrangling
    md = pd.read_csv(md_fp, sep=sep)
    distances_df = pd.read_csv(matrix_fp, sep='\t', index_col=0)

    # remove comment lines
    md = md[~ md['sample-id'].str.startswith('#')]

    bucket_col = 'Bucket'
    sample_type_col = 'SampleType'
    sample_id_col = 'sample-id'
    week_col = 'Composting Time Point'

    md[bucket_col].fillna(value=-1, inplace=True)
    md[bucket_col] = md[bucket_col].astype(int)
    md[week_col].fillna(value=-1, inplace=True)
    md[week_col] = md[week_col].astype(int)

    # keep only sample ids present in distance matrix
    md = md[md[sample_id_col].isin(distances_df.index)]

    # collect bucket sample ids of interest
    bucket_samples_df = md[
        (md[bucket_col] == bucket_id)
        & (md[sample_type_col] == bucket_sample_type)
    ]
    bucket_sample_ids = list(
        bucket_samples_df.sort_values(
            by=week_col, ascending=from_beginning
        )[sample_id_col].head(n)
    )

    # collect comparison ids of interest
    fecal_samples_df = md[md[sample_type_col] == 'Human Excrement']
    if compare_only_own_fecal:
        fecal_samples_df = fecal_samples_df[
            fecal_samples_df[bucket_col] == bucket_id
        ]
    fecal_sample_ids = list(
        fecal_samples_df[
            fecal_samples_df[sample_type_col] == 'Human Excrement'
        ][sample_id_col]
    )

    soil_sample_ids = list(
        md[md[sample_type_col] == 'Soil'][sample_id_col]
    )
    compost_sample_ids = list(
        md[md[sample_type_col] == 'Food Compost'][sample_id_col]
    )
    bulking_material_ids = list(
        md[md[sample_type_col] == 'Bulking Material'][sample_id_col]
    )

    # fetch all cells from the distance matrix and return
    distances = {
        'fecal': [],
        'soil': [],
        'food compost': [],
        'bulking material': [],
    }
    comps = {
        'fecal': fecal_sample_ids,
        'soil': soil_sample_ids,
        'food compost': compost_sample_ids,
        'bulking material': bulking_material_ids,
    }
    for bucket_sample_id in bucket_sample_ids:
        for comp, comp_ids in comps.items():
            for comp_id in comp_ids:
                distances[comp].append(
                    distances_df.at[bucket_sample_id, comp_id]
                )

    return distances


# python analysis.py path-to-output-dir
if __name__ == '__main__':
    for bucket_id in range(1, 17):
        out_path = sys.argv[1]
        os.makedirs(out_path, exist_ok=True)

        # change me
        distances = calculate_distances(
            md_fp='./data/nov-1-2024-metadata.tsv',
            matrix_fp='./data/nov-4-2024-distance-matrix.tsv',
            bucket_id=bucket_id,
            n=3,
            from_beginning=True,
            compare_only_own_fecal=False
        )

        fp = Path(out_path) / f'distances-bucket-{bucket_id}.json'
        with open(fp, 'w') as fh:
            json.dump(distances, fh)
