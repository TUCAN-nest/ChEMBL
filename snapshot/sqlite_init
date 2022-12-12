.headers on
.mode csv
.print Import data from snapshot file chembl_snapshot.csv
.import chembl_snapshot.csv chembl_snapshot


.print Attach original ChEMBL sqlite database
ATTACH DATABASE '../chembl_31/chembl_31_sqlite/chembl_31.db' AS chembl;


.print Export comounds that failed test_permutation_invariance
.output analysis_test_permutation_invariance_fails.csv
SELECT chembl_id, tucan
FROM chembl_snapshot
WHERE passed_test_permutation_invariance = "False";


.output
.print Export comounds that failed test_sumformula
.output analysis_test_sumformula_fails.csv
SELECT snapshot.chembl_id, snapshot.tucan, cp.full_molformula AS expected_sumformula_from_chembl
FROM chembl_snapshot snapshot
JOIN chembl.molecule_dictionary md ON snapshot.chembl_id = md.chembl_id
JOIN chembl.compound_properties cp ON md.molregno = cp.molregno
WHERE snapshot.passed_test_sumformula = "False";


.output
.print Export comounds that failed test_roundtrip_molfile_graph_tucan_graph_tucan_graph
.output analysis_test_roundtrip_molfile_graph_tucan_graph_tucan_graph.csv
SELECT chembl_id, tucan
FROM chembl_snapshot
WHERE passed_test_roundtrip_molfile_graph_tucan_graph_tucan_graph = "False";


.output
.print Create index on column 'chembl_snapshot.chembl_id' ...
CREATE INDEX idx_chembl_snapshot_chembl_id ON chembl_snapshot (chembl_id);


.print Create index on column 'chembl_snapshot.tucan' ...
CREATE INDEX idx_chembl_snapshot_tucan ON chembl_snapshot (tucan);


.print Export compounds with duplicate TUCAN strings
.output analysis_duplicate_tucan_strings.csv
SELECT chembl_id, tucan
FROM chembl_snapshot
WHERE tucan IN (
  SELECT tucan
  FROM chembl_snapshot
  GROUP BY tucan
  HAVING COUNT(tucan) > 1
)
ORDER BY tucan;


.output
.print Add column 'chembl_snapshot.standard_inchi_key' and fill it with data from the ChEMBL database
ALTER TABLE chembl_snapshot
ADD COLUMN standard_inchi_key VARCHAR(27);

UPDATE chembl_snapshot AS snapshot
SET standard_inchi_key = (
  SELECT cs.standard_inchi_key
  FROM chembl.compound_structures cs
  JOIN chembl.molecule_dictionary md ON md.molregno = cs.molregno
  WHERE snapshot.chembl_id = md.chembl_id
);


.print Add concatenation column 'chembl_snapshot.tucan_plus_inchi_key_first_layer' and fill it with data (concatenate TUCAN string and InChIKey first layer)
ALTER TABLE chembl_snapshot
ADD COLUMN tucan_plus_inchi_key_first_layer TEXT;

UPDATE chembl_snapshot
SET tucan_plus_inchi_key_first_layer = (
  SELECT snapshot.tucan || SUBSTR(snapshot.standard_inchi_key, 1, 14)
  FROM chembl_snapshot snapshot
  WHERE snapshot.chembl_id = chembl_snapshot.chembl_id
);


.print Export compounds with duplicate TUCAN strings, but exclude those with identical InChIKey first layer
.output analysis_duplicate_tucan_strings_different_inchikey.csv
SELECT chembl_id, tucan, standard_inchi_key
FROM chembl_snapshot
WHERE tucan IN (
  SELECT tucan FROM (
    SELECT tucan
    FROM chembl_snapshot
    GROUP BY tucan_plus_inchi_key_first_layer
    HAVING COUNT(tucan_plus_inchi_key_first_layer) = 1
  )
  GROUP BY tucan
  HAVING COUNT(tucan) > 1
)
ORDER BY tucan;


.output
.print Done
