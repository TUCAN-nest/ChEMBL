import sqlite3
from rdkit import Chem

select_molfile_query = """
    SELECT cs.rowid, cs.molfile, md.chembl_id, cp.full_molformula
    FROM compound_structures cs
    JOIN molecule_dictionary md ON cs.molregno = md.molregno
    JOIN compound_properties cp ON cs.molregno = cp.molregno
    WHERE cs.rowid BETWEEN ? AND ?
    """


def create_sdf(db_filename: str, output_filename: str, first_row: int, last_row: int):
    """Selects a certain region of the table 'compound_structures' and creates an
    SDFile from the compounds' molfiles. Additionally, implicit hydrogens are
    added and the ChEMBL ID, the sum formula (Hill format) and the row ID are
    attached to each SDFile entry. The region of the table is selected via the
    given range of rows.
    """
    con = sqlite3.connect(f"file:{db_filename}?mode=ro", uri=True)

    with Chem.SDWriter(output_filename) as writer:
        writer.SetForceV3000(True)
        for rowid, molfile, chembl_id, full_molformula in con.execute(select_molfile_query, (first_row, last_row)):
            mol = Chem.MolFromMolBlock(molfile)
            mol = Chem.AddHs(mol)
            mol.SetProp("chembl_id", chembl_id)
            mol.SetProp("full_molformula", full_molformula)
            mol.SetProp("row_id", str(rowid))
            writer.write(mol)
