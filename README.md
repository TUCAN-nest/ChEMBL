# Test TUCAN with the ChEMBL compounds database

## Snapshot generation using Snakemake in Docker
Build Docker image with all necessary dependencies:
```
docker build -t tucan/chembl-test - < Dockerfile
```
Run Snakemake to generate the snapshot file:
```
docker run -v $(pwd):/ChEMBL-test -it --rm tucan/chembl-test snakemake -j all --snakefile Snakefile_ChEMBL snapshot
```
Remove Docker image:
```
docker rmi tucan/chembl-test
```
