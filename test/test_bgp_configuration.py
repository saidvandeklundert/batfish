"""
python -m pytest test/test_bgp_configuration.py 
"""
from tabulate import tabulate


def test_external_peers_no_empty_import_policies(different_as):
    """
    Check if there are BGP sessions with differing AS-numbers that
     have no import policy applied.
    """
    no_import_policy = different_as["Import_Policy"] == "[]"
    df = different_as[no_import_policy]
    offending_peers = df[["Node", "Remote_IP"]]
    tabulate(df, headers="keys", tablefmt="psql")
    assert df.empty, f"eBGP sessions without import policy:\n{offending_peers}"


def test_send_community_border_false():
    pass
