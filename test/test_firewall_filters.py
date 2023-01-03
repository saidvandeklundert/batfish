"""
python -m pytest test/test_firewall_filters.py 
"""

import pytest
from pybatfish.datamodel.flow import HeaderConstraints


@pytest.mark.parametrize(
    "acl_name",
    [
        ("ISOLATE"),
        ("MGMT"),
    ],
)
def test_acl_exists(named_structures, all_nodes, acl_name):
    """Verify certain ACLs exist on every node"""
    acl_missing_on_nodes = []
    for node in all_nodes:
        acls_on_node = named_structures[named_structures["Node"] == node]
        if acl_name not in acls_on_node["Structure_Name"].values:
            acl_missing_on_nodes.append(node)
    assert (
        len(acl_missing_on_nodes) == 0
    ), f"ACL TEST is missing on the following nodes: {acl_missing_on_nodes}"


def test_should_be_allowed(bf):
    """
    Asserts we can ssh into 2.1.1.1/28 while sourcing traffic from 192.168.1.0/24.

    Will execute the test on every node where the 'MGMT_EXAMPLE' is present.
    """
    ssh_flow = HeaderConstraints(
        srcIps="192.168.1.0/24", dstIps="2.1.1.1/28", applications=["ssh"]
    )
    df = bf.q.testFilters(headers=ssh_flow, filters="MGMT_EXAMPLE").answer().frame()
    # import pdb

    # pdb.set_trace()
    assert all(action == "PERMIT" for action in df["Action"].values), df[
        df["Action"] != "PERMIT"
    ][["Node", "Action"]]


@pytest.mark.parametrize(
    "source",
    [
        ("192.168.2.0/24"),
        ("66.0.0.0/24"),
        ("6.0.0.0/24"),
    ],
)
def test_should_not_be_allowed(bf, source):
    """
    Asserts we cannot ssh into 2.1.1.1/28 while sourcing traffic the sources
    we let pytest parametrize.

    Will execute the test on every node where the 'MGMT_EXAMPLE' is present.
    """
    ssh_flow = HeaderConstraints(
        srcIps=source, dstIps="2.1.1.1/28", applications=["ssh"]
    )
    df = bf.q.testFilters(headers=ssh_flow, filters="MGMT_EXAMPLE").answer().frame()
    assert all(action == "PERMIT" for action in df["Action"].values), df[
        df["Action"] != "PERMIT"
    ]
