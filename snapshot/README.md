# ChEMBL snapshot file
* ChEMBL version: [31](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_31/)
* TUCAN commit hash: [ec13180c4b299759c5b0a00d3b7803893523b437](https://github.com/TUCAN-nest/TUCAN/commit/ec13180c4b299759c5b0a00d3b7803893523b437)
* Python version (`python --version`): 3.10.6
* Snakemake version (`snakemake --version`): 7.18.2+0.ga5c35239.dirty
* RDKit version (`pip show rdkit`): 2022.9.2

## Analysis pipeline
Analysis of the snapshot file happens in a SQLite database using the instructions in _[analysis.sql](analysis.sql)_ (a mix of SQLite meta-commands and SQL statements). The analysis' results are written into separate csv files, which are not added to this repository.

Requirements:
- sqlite3
- The ChEMBL SQLite database is expected to be present in `../chembl_31/chembl_31_sqlite/chembl_31.db` (as downloaded and extracted by the [Snakemake workflow](../Snakefile_ChEMBL)).

To run the analysis pipeline:
- in-memory: `sqlite3 ":memory:" < analysis.sql` (uses about 8.2 GB of memory)
- on-disk: `sqlite3 analysis.db < analysis.sql`

## Licensing and Attribution
This snapshot file is covered by the _Creative Commons Attribution-ShareAlike 4.0 International_ (CC BY-SA 4.0) license (see _[LICENSE](LICENSE)_ file).

The snapshot file is a derivate work of the [ChEMBL database release](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/), which is licensed by the _Creative Commons Attribution-ShareAlike 3.0 Unported_ (CC BY-SA 3.0) license.

**Attribution for the ChEMBL database release:**

Mendez D, Gaulton A, Bento AP, Chambers J, De Veij M, Félix E, Magariños MP, Mosquera JF, Mutowo P, Nowotka M, Gordillo-Marañón M, Hunter F, Junco L, Mugumbate G, Rodriguez-Lopez M, Atkinson F, Bosc N, Radoux CJ, Segura-Cabrera A, Hersey A, Leach AR. ChEMBL: towards direct deposition of bioassay data. Nucleic Acids Res. 2019 47(D1):D930-D940. DOI: 10.1093/nar/gky1075
