"""
python -m pytest test/test_bgp_configuration.py 
"""


def test_external_peers_no_empty_import_policies(different_as):
    """
    Check if there are eBGP sessions have no import policy applied.
    """
    no_import_policy = different_as[different_as["Import_Policy"].str.len() == 0]
    potential_offenders = no_import_policy[["Node", "Remote_IP"]]
    assert (
        no_import_policy.empty
    ), f"eBGP sessions without import policy:\n{potential_offenders}"


def test_external_peers_have_specific_import_policy_applied(different_as):
    """
    Verify all eBGP sessions have 'internet-edge' applied on import.
    """
    nodes_without_import_policy = different_as[
        different_as.apply(
            lambda row: "internet-edge" not in list(row["Import_Policy"]),
            axis=1,
        )
    ]

    assert (
        nodes_without_import_policy.empty
    ), f"eBGP with missing import policy 'internet-edge':\n{nodes_without_import_policy}"


def test_ibgp_session_status(bf):
    """
    Verify iBGP sessions can reach the ESTABLISHED state.
    """
    df = bf.q.bgpSessionStatus().answer().frame()

    same_as = df["Remote_AS"].astype(int) == df["Local_AS"]
    node_status = df[same_as][["Node", "Established_Status"]]
    not_established = node_status[node_status["Established_Status"] != "ESTABLISHED"]
    assert not_established.empty
