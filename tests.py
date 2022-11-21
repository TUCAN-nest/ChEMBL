from tucan.canonicalization import canonicalize_molecule
from tucan.serialization import serialize_molecule
from tucan.io import graph_from_molfile_text
from tucan.graph_utils import permute_molecule
import random
from rdkit import Chem


# from TUCAN/tests/test_canonicalization.py
def test_invariance(molfile, chembl_id, n_runs=10, random_seed=random.random()):
    m = graph_from_molfile_text(molfile)

    m_canon = canonicalize_molecule(m)
    m_serialized = serialize_molecule(m_canon)
    random.seed(random_seed)
    for _ in range(n_runs):
        permutation_seed = random.random()
        m_permu = permute_molecule(m, random_seed=permutation_seed)
        m_permu_canon = canonicalize_molecule(m_permu)
        m_permu_serialized = serialize_molecule(m_permu_canon)
        if m_serialized != m_permu_serialized:
            return "invariance test failed for %s\n" % chembl_id
    return ""


def exec_invariance_test_for_molecule(molfile, output, chembl_id):
    result = test_invariance(molfile, chembl_id)
    with open(output, "a") as file:
        file.write(result)


def exec_tests_for_chunk(input_sdfile, output_log):
    supplier = Chem.SDMolSupplier(fileName=input_sdfile, removeHs=False)
    for molecule in supplier:
        molfile = Chem.MolToMolBlock(mol=molecule, forceV3000=True)
        chembl_id = molecule.GetProp("chembl_id")
        exec_invariance_test_for_molecule(molfile, output_log, chembl_id)
