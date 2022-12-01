import csv
import re
from rdkit import Chem
from tucan.canonicalization import canonicalize_molecule
from tucan.io import graph_from_molfile_text
from tucan.serialization import serialize_molecule
from tucan.test_utils import permutation_invariance, roundtrip_graph_tucan_graph_tucan_graph


def exec_tests_for_chunk(input_sdfile: str, output_csv: str, add_header: bool):
    supplier = Chem.SDMolSupplier(fileName=input_sdfile, removeHs=False)

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = [
            "chembl_id",
            "tucan",
            "passed_test_permutation_invariance",
            "passed_test_sumformula",
            "passed_test_roundtrip_molfile_graph_tucan_graph_tucan_graph"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if add_header:
            writer.writeheader()

        for mol in supplier:
            molfile = Chem.MolToMolBlock(mol=mol, forceV3000=True)
            result = {}

            result["chembl_id"] = mol.GetProp("chembl_id")
            result["tucan"] = tucan = _molfile_to_tucan(molfile)
            result["passed_test_permutation_invariance"] = _test_permutation_invariance(molfile)
            result["passed_test_sumformula"] = _test_sumformula(tucan, mol.GetProp("full_molformula"))
            result[
                "passed_test_roundtrip_molfile_graph_tucan_graph_tucan_graph"
            ] = _test_roundtrip_molfile_graph_tucan_graph_tucan_graph(molfile)

            writer.writerow(result)


def _molfile_to_tucan(molfile: str) -> str:
    return serialize_molecule(canonicalize_molecule(graph_from_molfile_text(molfile)))


def _test_permutation_invariance(molfile: str) -> bool:
    m = graph_from_molfile_text(molfile)
    try:
        permutation_invariance(m)
        return True
    except AssertionError:
        return False


def _test_sumformula(tucan: str, full_molformula_from_chembl: str) -> bool:
    sumformula_from_tucan = tucan.split("/")[0]
    return sumformula_from_tucan == _prune_charge(full_molformula_from_chembl)


def _prune_charge(molformula: str) -> str:
    return re.split("[-+]", molformula)[0]


def _test_roundtrip_molfile_graph_tucan_graph_tucan_graph(molfile: str) -> bool:
    m = graph_from_molfile_text(molfile)
    try:
        roundtrip_graph_tucan_graph_tucan_graph(m)
        return True
    except AssertionError:
        return False
