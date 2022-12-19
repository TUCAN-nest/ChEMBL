FROM snakemake/snakemake:stable

RUN set -ex && \
	pip install git+https://github.com/TUCAN-nest/TUCAN.git rdkit

WORKDIR /ChEMBL-test
