# gut-to-soil-manuscript-figures

A [QIIME 2](https://qiime2.org) "Single-Use Plugin" (SUP) [developed](https://develop.qiime2.org) by Liz Gehret (elizabeth.gehret@nau.edu). 🔌

## Installation instructions

### Install Prerequisites

[Miniconda](https://conda.io/miniconda.html) provides the `conda` environment and package manager, and is currently the only supported way to install QIIME 2.
Follow the instructions for downloading and installing Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of `conda`:

```bash
conda update conda
```

###  Install development version of `gut-to-soil-manuscript-figures`

Next, you need to get into the top-level `gut-to-soil-manuscript-figures` directory.
You can achieve this by [cloning the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
Once you have the repository on your computer, change (`cd gut-to-soil-manuscript-figures`) into the local directory.

If you're in an existing conda environment, deactivate it by running `conda deactivate`.


Then, run:

```shell
conda env create -n gts-manuscript-figs-dev --file ./environments/gut-to-soil-manuscript-figures-qiime2-tiny-2024.5.yml
```

After this completes, activate the new environment you created by running:

```shell
conda activate gts-manuscript-figs-dev
```

After completing the install steps above, confirm that everything is working as expected by running:

```shell
qiime info
```

This will provide you with a sanity check for the expected packages within your conda environment.

You should see the following system info:
```
Python version: 3.9
QIIME 2 release: 2024.5
QIIME 2 version: 2024.5.1
q2cli version: 2024.5.0
```

Additionally, you should see the following list of plugins present:
```
diversity
diversity-lib
emperor
feature-table
gut-to-soil-manuscript-figures
metadata
types
```

If all of the above matches what you're seeing locally, you're ready to use this plugin!

You should be able to review the help text by running:

```shell
qiime gut-to-soil-manuscript-figures pcoa-2d --help
```

Here's an example workflow, based on what was used to generate the PCoA figures in Jeff Meilander's manuscript.

Your first step will be filtering the distance matrix you'd like to use for the PCoA plot so that it only contains the sample types of interest.
```
qiime diversity filter-distance-matrix \
--i-distance-matrix unweighted-unifrac-distance-matrix.qza \
--m-metadata-file final-analysis-metadata.tsv \
--p-where "[SampleType] IN ('Soil', 'Food Compost', 'Landscape Compost', 'Human Excrement', 'Human Excrement Compost', 'Bulking Material')" \
--o-filtered-distance-matrix filtered-unweighted-unifrac-distance-matrix.qza
```

Next, you'll turn this distance matrix into a two-dimensional PCoAResults object, which will be used as input for the pcoa plot.
```
qiime diversity pcoa \
--i-distance-matrix filtered-unweighted-unifrac-distance-matrix.qza \
--p-number-of-dimensions 2 \
--o-pcoa filtered-unweighted-unifrac-2d-pcoa.qza
```

Now we're ready to generate a pcoa plot!
```
qiime gut-to-soil-manuscript-figures pcoa-2d \
--i-ordination filtered-unweighted-unifrac-2d-pcoa.qza \
--m-metadata-file final-analysis-metadata.tsv \
--p-measure 'Unweighted UniFrac' \
--p-average \
--p-export-legend \
--p-highlighted-buckets '3, 4' \
--o-visualization buckets34-pcoa.qzv
```

Note that all of the above filenames were used as an example.
Please replace the inputs with your specific distance matrix and metadata files!

## About

The `gut-to-soil-manuscript-figures` Python package was [created from a template](https://develop.qiime2.org/en/latest/plugins/tutorials/create-from-template.html).
To learn more about `gut-to-soil-manuscript-figures`, refer to the [project website](https://github.com/caporaso-lab/gut-to-coil-manuscript-figures/).
To learn how to use QIIME 2, refer to the [QIIME 2 User Documentation](https://docs.qiime2.org).
To learn QIIME 2 plugin development, refer to [*Developing with QIIME 2*](https://develop.qiime2.org).

`gut-to-soil-manuscript-figures` is a QIIME 2 community plugin, meaning that it is not necessarily developed and maintained by the developers of QIIME 2.
Please be aware that because community plugins are developed by the QIIME 2 developer community, and not necessarily the QIIME 2 developers themselves, some may not be actively maintained or compatible with current release versions of the QIIME 2 distributions.
More information on development and support for community plugins can be found [here](https://library.qiime2.org).
If you need help with a community plugin, first refer to the [project website](https://github.com/caporaso-lab/gut-to-coil-manuscript-figures/).
If that page doesn't provide information on how to get help, or you need additional help, head to the [Community Plugins category](https://forum.qiime2.org/c/community-contributions/community-plugins/14) on the QIIME 2 Forum where the QIIME 2 developers will do their best to help you.
