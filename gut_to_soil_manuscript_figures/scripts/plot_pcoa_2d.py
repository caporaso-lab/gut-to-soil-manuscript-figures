#!/usr/bin/python3

import sys
import skbio
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


# HELPER METHODS
# util for converting sample IDs to ordination XY coords & swapping axes
def _swap_axis(df, sample_type, swap):
    if swap == 'False':
        x = df.loc[sample_type][0]
        y = df.loc[sample_type][1]
    elif swap == 'True':
        x = df.loc[sample_type][1]
        y = df.loc[sample_type][0]
    else:
        raise ValueError('Invalid selection for `swap_axes` parameter.'
                         ' Must either be `True` or `False`.')

    return x, y


# util for highlighted bucket handling
def _bucket_util(highlighted_buckets, md, ord_2d):
    # handles multiple buckets being entered via command line/jupyter notebook
    # entire input for this command is a string, split on commas
    if ',' in highlighted_buckets:
        bucket_list = [float(x) for x in highlighted_buckets.split(',')]
    else:
        bucket_list = [float(highlighted_buckets)]

    # empty dicts to be filled with details for each bucket's time series
    # details & then starting details (i.e. HE & bulking)
    buckets_dict = {}
    bucket_starts_dict = {}

    for bucket in bucket_list:
        # sorting the MD by week for line plot
        # connecting time series data in order
        md_bucket_sorted = \
            md[(md['Bucket'] == bucket) &
               (md['SampleType2'] == 'Compost Post-Roll')].sort_values('Week')

        # week 1-52 IDs for selected bucket
        bucket_ids_sorted = \
            md_bucket_sorted[md_bucket_sorted['Week'] > 0.0].index.values

        # making sure bucket IDs used are only ones that are present in both
        # the md and ordination results
        bucket_ids = []
        for i in bucket_ids_sorted:
            if i in ord_2d.index.values:
                bucket_ids.append(i)

        buckets_dict[bucket] = bucket_ids

        # week 0 i.e. inputs for dotted line connecting HE & bulking -> HEC
        # HE
        bucket_ids_HE_week0 = \
            md[(md['Bucket'] == bucket) &
               (md['SampleType2'] == 'Self Sample') &
               (md['Week'] == 0.0)].index.values

        ids_HE_week0 = []
        for i in bucket_ids_HE_week0:
            if i in ord_2d.index.values:
                ids_HE_week0.append(i)

        # bulking
        bucket_ids_bulk_week0 = \
            md[(md['Bucket'] == bucket) &
               (md['SampleType2'] == 'Bulking Material') &
               (md['Week'] == 0.0)].index.values

        ids_bulk_week0 = []
        for i in bucket_ids_bulk_week0:
            if i in ord_2d.index.values:
                ids_bulk_week0.append(i)

        # week 1 i.e. end points for dotted line connecting HE & BM -> HEC
        bucket_ids_HEC_week1 = \
            md_bucket_sorted[md_bucket_sorted['Week'] == 1.0].index.values

        ids_HEC_week1 = []
        for i in bucket_ids_HEC_week1:
            if i in ord_2d.index.values:
                ids_HEC_week1.append(i)

        # nested dict for each bucket start info: HE week0, bulking, HEC week1
        bucket_starts_dict[bucket] = {
            'HE_week0': [i for i in ids_HE_week0],
            'bulk_week0': [i for i in ids_bulk_week0],
            'HEC_week1': [i for i in ids_HEC_week1]
        }

    selected_buckets_ids = [i for i in buckets_dict.values()]
    bucket_set = {i for lst in selected_buckets_ids for i in lst}

    return buckets_dict, selected_buckets_ids, bucket_set, bucket_starts_dict


# MAIN METHOD #
def plot_pcoa_2d(metadata_fp, ordination_fp, measure,
                 average, week_annotations, save_as,
                 invert_x, invert_y, swap_axes,
                 himalaya, pit_toilet,
                 highlighted_buckets=None):

    ord_rslts = skbio.OrdinationResults.read(str(ordination_fp))
    ord_2d = ord_rslts.samples.iloc[:, 0:2]

    metadata_in = pd.read_csv(str(metadata_fp),
                              sep='\t').set_index('sample-id')
    # filtering metadata to only include samples w/IDs present in ordination
    metadata = metadata_in.loc[ord_2d.index.values]

    # setting XY labels based on swap axis &
    # figure aspect based on proportion explained
    if swap_axes == 'True':
        fig_aspect = \
            ord_rslts.proportion_explained[0]/ord_rslts.proportion_explained[1]
        x_label = 2
        y_label = 1
    elif swap_axes == 'False':
        fig_aspect = \
            ord_rslts.proportion_explained[1]/ord_rslts.proportion_explained[0]
        x_label = 1
        y_label = 2
    else:
        raise ValueError('Invalid value for `swap_axes` parameter.'
                         ' Must be either `True` or `False`.')

    # invering XY axis based on x and/or y invert
    if invert_x == 'True':
        ord_2d[0] = ord_2d[0].multiply(-1)
    if invert_y == 'True':
        ord_2d[1] = ord_2d[1].multiply(-1)

    # allowed sample types to be pulled from the md
    sample_types = ['EMP-Soils', 'Food-Compost', 'Self Sample',
                    'Compost Post-Roll', 'Bulking Material', 'Pit Toilet']

    # if using himalaya and/or pit toilet data
    if himalaya == 'True':
        sample_types.append('Himalaya')
    if pit_toilet == 'True':
        sample_types.append('Pit Toilet')

    # sorting the filtered md (by allowed sample types) by week
    md = metadata[metadata['SampleType2']
                  .isin(sample_types)].sort_values('Week')
    md['Bucket'] = md['Bucket'].astype(float)
    md['Week'] = md['Week'].astype(float)

    buckets_md = md[md['Bucket'].between(1, 16)]

    # ALL SUBJECT FECAL SAMPLES: IDs -> XY ordination points
    fecal_ids = list(set(buckets_md[buckets_md['Week'] == 0.0].index.values) &
                     set(ord_2d.index.values))
    x_fecal, y_fecal = _swap_axis(ord_2d, fecal_ids, swap_axes)

    # ALL SUBJECT BULKING MATERIAL: IDs -> XY ordination points
    bulking_ids = \
        list(set(md[md['SampleType2'] == 'Bulking Material'].index.values) &
             set(ord_2d.index.values))
    x_bulking, y_bulking = _swap_axis(ord_2d, bulking_ids, swap_axes)

    # (OPTIONAL) SELECTED BUCKET(S): IDs -> XY ordination points
    if highlighted_buckets:
        buckets_dict, selected_buckets_ids, bucket_set, bucket_starts_dict = \
            _bucket_util(highlighted_buckets, md, ord_2d)

    # (OPTIONAL) WEEKLY MEAN FOR ALL BUCKETS: IDs -> XY ordination points
    if average == 'True':
        weeks_md = md[md['Week'].between(1, 52)]
        weeks = list(set(weeks_md['Week'].values))

        # dicts for each week's mean x&y values
        bucket_weekly_avgs_x = {}
        bucket_weekly_avgs_y = {}

        for week in weeks:
            x_list = []
            y_list = []

            # filtering the md to only include post-roll sample types
            weekly_bucket_ids = \
                md[(md['Week'] == week) &
                    (md['SampleType2'] == 'Compost Post-Roll')].index.values

            # only use IDs that are present both in the md and ordination
            included_ids = []
            for i in weekly_bucket_ids:
                if i in ord_2d.index.values:
                    included_ids.append(i)

            # grab weeks 1 & 52 separately to annotate 'start' and 'end' points
            # for selected bucket(s) and weekly mean for all buckets
            if week == 1.0:
                x1, y1 = _swap_axis(ord_2d, included_ids, swap_axes)
                x1_mean = np.mean(x1.values)
                y1_mean = np.mean(y1.values)
            elif week == 52.0:
                x52, y52 = _swap_axis(ord_2d, included_ids, swap_axes)
                x52_mean = np.mean(x52.values)
                y52_mean = np.mean(y52.values)
            else:
                pass

            # making sure x&y values correspond to correct ordination axis
            if swap_axes == 'False':
                x_list.append(ord_2d.loc[included_ids][0].values)
                y_list.append(ord_2d.loc[included_ids][1].values)
            elif swap_axes == 'True':
                x_list.append(ord_2d.loc[included_ids][1].values)
                y_list.append(ord_2d.loc[included_ids][0].values)
            else:
                raise ValueError('Invalid selection for `swap_axes` parameter.'
                                 ' Must either be `True` or `False`.')

            x_avg = np.mean(x_list)
            bucket_weekly_avgs_x[week] = x_avg

            y_avg = np.mean(y_list)
            bucket_weekly_avgs_y[week] = y_avg

        # only calculate mean for HE & bulking wk 0 if
        # no highlighted bucket is selected
        if not highlighted_buckets:
            # HE wk 0 mean
            HE_week0 = \
                md[(md['SampleType2'] == 'Self Sample') &
                   (md['Week'] == 0.0)].index.values
            ids_HE_week0 = []
            for i in HE_week0:
                if i in ord_2d.index.values:
                    ids_HE_week0.append(i)
            x0_HE, y0_HE = _swap_axis(ord_2d, ids_HE_week0, swap_axes)
            x0_HE_mean = np.mean(x0_HE)
            y0_HE_mean = np.mean(y0_HE)

            # bulk wk 0 mean
            bulk_week0 = \
                md[(md['SampleType2'] == 'Bulking Material') &
                   (md['Week'] == 0.0)].index.values
            ids_bulk_week0 = []
            for i in bulk_week0:
                if i in ord_2d.index.values:
                    ids_bulk_week0.append(i)
            x0_bulk, y0_bulk = _swap_axis(ord_2d, ids_bulk_week0, swap_axes)
            x0_bulk_mean = np.mean(x0_bulk)
            y0_bulk_mean = np.mean(y0_bulk)

    # ALL BUCKETS (minus highlighted bucket(s))
    all_bucket_ids_w_fecal = \
        list(set(md[md['Bucket'].between(1, 16)].index.values) &
             set(ord_2d.index.values))
    all_bucket_ids = list(set(all_bucket_ids_w_fecal) - set(fecal_ids))

    if highlighted_buckets:
        bucket_ids = list(set(all_bucket_ids) - bucket_set)
    else:
        bucket_ids = list(set(all_bucket_ids))
    x_buckets, y_buckets = _swap_axis(ord_2d, bucket_ids, swap_axes)

    # EMP SOILS
    emp_ids = md.loc[md['Bucket'] == 0.0].index.values
    x_emp, y_emp = _swap_axis(ord_2d, emp_ids, swap_axes)

    # FOOD COMPOST
    compost_ids = \
        list(set(md.loc[md['Bucket'] == 17.0].index.values) &
             set(ord_2d.index.values))
    x_compost, y_compost = _swap_axis(ord_2d, compost_ids, swap_axes)

    # (OPTIONAL SAMPLE TYPES) HIMALAYA
    if himalaya == 'True':
        hima_ids = md.loc[md['Bucket'] == 18.0].index.values
        x_hima, y_hima = _swap_axis(ord_2d, hima_ids, swap_axes)

    # (OPTIONAL SAMPLE TYPES) PIT TOILET
    if pit_toilet == 'True':
        pt_ids = md.loc[md['Bucket'] == 19.0].index.values
        x_pt, y_pt = _swap_axis(ord_2d, pt_ids, swap_axes)

    # Setting up the plot & axis
    fig, ax = plt.subplots(1, 1, figsize=(15, 8))
    ax.set_aspect(aspect=fig_aspect)

    # DEFINING THE COLORMAP FOR EACH SELECTED BUCKET
    if highlighted_buckets:
        color_idx = np.linspace(0, 1, len(buckets_dict))
        color_dict = dict(zip(buckets_dict.keys(), color_idx))
        viridis = mpl.colormaps['viridis'].resampled(len(buckets_dict))

    # Fecal - all subjects
    fecal_scatter = \
        plt.scatter(x=x_fecal, y=y_fecal, facecolors='none',
                    edgecolors='tab:brown',
                    label='HE (other subjects)')

    # Bulking Material - all subjects
    bulking_scatter = \
        plt.scatter(x=x_bulking, y=y_bulking, facecolors='none',
                    edgecolors='g', label='Bulking Material (other subjects)')

    # All buckets (minus highlighted bucket(s))
    all_sample_buckets = \
        plt.scatter(x=x_buckets, y=y_buckets, facecolors='none',
                    edgecolors='#C5C9C7', marker='^',
                    label='HEC (other subjects)')

    # (OPTIONAL) Weekly Mean for all Buckets
    if average == 'True':
        bucket_avgs_scatter = \
            plt.scatter(x=bucket_weekly_avgs_x.values(),
                        y=bucket_weekly_avgs_y.values(),
                        marker='*', facecolors='#1f77b4',
                        s=100, label='HEC (Weekly Mean)')

        # adding HE mean if only plotting the weekly mean
        # (w/o any highlighted bucket(s))
        if not highlighted_buckets:
            # HE
            HE_week0_scatter = \
                plt.scatter(x=x0_HE_mean, y=y0_HE_mean,
                            marker='*', s=150, zorder=1,
                            facecolors='tab:brown', edgecolors='k',
                            label='HE (Weekly Mean)')

            # bulking
            bulk_week0_scatter = \
                plt.scatter(x=x0_bulk_mean, y=y0_bulk_mean,
                            marker='*', s=150, zorder=1,
                            facecolors='g', edgecolors='k',
                            label='Bulking Material (Weekly Mean)')

    # EMP Soil
    emp_soil_scatter = plt.scatter(x=x_emp, y=y_emp,
                                   facecolors='k', label='Soil')

    # Food Compost
    food_compost_scatter = plt.scatter(x=x_compost, y=y_compost,
                                       facecolors='r',
                                       label='Food and Yard Waste Compost')

    # (OPTIONAL SAMPLE TYPES) Himalaya
    if himalaya == 'True':
        himalaya_scatter = plt.scatter(x=x_hima, y=y_hima,
                                       facecolors='b', label='Himalaya')

    # (OPTIONAL SAMPLE TYPES) Pit Toilet
    if pit_toilet == 'True':
        pit_toilet_scatter = plt.scatter(x=x_pt, y=y_pt,
                                         facecolors='y', label='Pit Toilet')

    # collecting the handle info to add to the legend
    bucket_handles = []
    bucket_nums = []

    # (OPTIONAL) HIGHLIGHTED BUCKET(S)
    if highlighted_buckets:
        # adding start info (HE, bulking -> HEC wk1) for highlighted bucket(s)
        for bucket, ids in bucket_starts_dict.items():
            if swap_axes == 'False':
                x0_HE = ord_2d.loc[ids['HE_week0']][0]
                y0_HE = ord_2d.loc[ids['HE_week0']][1]

                x0_bulk = ord_2d.loc[ids['bulk_week0']][0]
                y0_bulk = ord_2d.loc[ids['bulk_week0']][1]

                x1_HEC = ord_2d.loc[ids['HEC_week1']][0]
                y1_HEC = ord_2d.loc[ids['HEC_week1']][1]

            elif swap_axes == 'True':
                x0_HE = ord_2d.loc[ids['HE_week0']][1]
                y0_HE = ord_2d.loc[ids['HE_week0']][0]

                x0_bulk = ord_2d.loc[ids['bulk_week0']][1]
                y0_bulk = ord_2d.loc[ids['bulk_week0']][0]

                x1_HEC = ord_2d.loc[ids['HEC_week1']][1]
                y1_HEC = ord_2d.loc[ids['HEC_week1']][0]

            for x, y in zip(x0_HE, y0_HE):
                ax.plot([x, float(x1_HEC.values)],
                        [y, float(y1_HEC.values)],
                        '--', color='#C5C9C7',
                        linewidth=0.75, zorder=1)

            for x, y in zip(x0_bulk, y0_bulk):
                ax.plot([x, float(x1_HEC.values)],
                        [y, float(y1_HEC.values)],
                        '--', color='#C5C9C7',
                        linewidth=0.75, zorder=1)

            HE_week0_scatter = \
                plt.scatter(x=x0_HE, y=y0_HE, facecolors='tab:brown',
                            label=f'HE (Subject #{bucket})')
            bucket_handles.append(HE_week0_scatter)

            bulk_week0_scatter = \
                plt.scatter(x=x0_bulk, y=y0_bulk, facecolors='g',
                            label=f'Bulking Material (Subject #{bucket})')
            bucket_handles.append(bulk_week0_scatter)

        for bucket, ids in buckets_dict.items():
            x_bucket, y_bucket = _swap_axis(ord_2d, ids, swap_axes)

            ax.plot(x_bucket, y_bucket, color='k', zorder=1)

            highlighted_bucket_scatter = \
                plt.scatter(x=x_bucket, y=y_bucket,
                            facecolors=viridis(color_dict[bucket]),
                            edgecolors='k', marker='^',
                            label=f'HEC (Subject #{bucket})')

            bucket_handles.append(highlighted_bucket_scatter)
            bucket_nums.append(bucket)

            # adding week annotations for each highlighted bucket
            if week_annotations == 'True':
                for week, x, y in zip((md.loc[ids]['Week']),
                                      x_bucket, y_bucket):
                    week_int = int(week)
                    ax.annotate(str(week_int), weight='bold', color='purple',
                                xy=(x, y), xytext=((x+0.002), (y+0.002)))
            elif week_annotations == 'False':
                # adding start/end notations for each highlighted bucket
                ax.annotate('Start', weight='bold', color='purple',
                            xy=(x_bucket[0], y_bucket[0]),
                            xytext=((x_bucket[0]+0.002),
                                    (y_bucket[0]+0.002)))
                ax.annotate('End', weight='bold', color='purple',
                            xy=(x_bucket[-1], y_bucket[-1]),
                            xytext=((x_bucket[-1]+0.005),
                                    (y_bucket[-1]+0.002)))

    # appending legend info for non-highlighted subject data
    bucket_handles.append(fecal_scatter)
    bucket_handles.append(bulking_scatter)
    bucket_handles.append(all_sample_buckets)

    if average == 'True':
        if not highlighted_buckets:
            bucket_handles.append(HE_week0_scatter)
            bucket_handles.append(bulk_week0_scatter)
        bucket_handles.append(bucket_avgs_scatter)

    bucket_handles.append(food_compost_scatter)
    bucket_handles.append(emp_soil_scatter)

    if himalaya == 'True':
        bucket_handles.append(himalaya_scatter)

    if pit_toilet == 'True':
        bucket_handles.append(pit_toilet_scatter)

    # (OPTIONAL) Weekly Mean for all Buckets
    if average == 'True':
        ax.plot(bucket_weekly_avgs_x.values(),
                bucket_weekly_avgs_y.values(), color='#1f77b4')
        ax.annotate('Start', weight='bold', xy=(x1_mean, y1_mean),
                    xytext=((x1_mean+0.002), (y1_mean+0.002)))
        ax.annotate('End', weight='bold', xy=(x52_mean, y52_mean),
                    xytext=((x52_mean+0.005), (y52_mean+0.002)))

        if not highlighted_buckets:
            ax.plot([x0_HE_mean, x1_mean], [y0_HE_mean, y1_mean],
                    '--', color='#C5C9C7', linewidth=0.75, zorder=2)
            ax.plot([x0_bulk_mean, x1_mean], [y0_bulk_mean, y1_mean],
                    '--', color='#C5C9C7', linewidth=0.75, zorder=2)

    # Adding title, labels & legend details
    plt.gca().set(xlabel=f'PCOA {x_label}', ylabel=f'PCOA {y_label}',
                  title=f'2D {measure} for Subject(s) {bucket_nums}',
                  label='Subject#')

    # HELPER METHOD FOR EXPORTING LEGEND AS A SEPARATE FIGURE - leave as-is
    # ax.set_title('Subject 10.0', loc='left')

    # def export_legend(legend, filename='legend.png'):
    #     fig = legend.figure
    #     fig.canvas.draw()
    #     bbox = legend.get_window_extent().transformed(
    #         fig.dpi_scale_trans.inverted())
    #     fig.savefig(filename, dpi='figure', bbox_inches=bbox)

    # legend = plt.legend(handles=bucket_handles, fontsize=12)
    # export_legend(legend)
    # legend.remove()

    plt.legend(handles=bucket_handles, bbox_to_anchor=(1.1, 1.05))
    plt.tight_layout()
    plt.savefig(str(save_as), bbox_inches='tight')


if __name__ == '__main__':
    metadata_fp = sys.argv[1]
    ordination_fp = sys.argv[2]
    measure = sys.argv[3]
    average = sys.argv[4]
    week_annotations = sys.argv[5]
    save_as = sys.argv[6]
    invert_x = sys.argv[7]
    invert_y = sys.argv[8]
    swap_axes = sys.argv[9]
    himalaya = sys.argv[10]
    pit_toilet = sys.argv[11]
    highlighted_buckets = sys.argv[12]

    plot_pcoa_2d(metadata_fp, ordination_fp, measure,
                 average, week_annotations, save_as,
                 invert_x, invert_y, swap_axes,
                 himalaya, pit_toilet,
                 highlighted_buckets)
