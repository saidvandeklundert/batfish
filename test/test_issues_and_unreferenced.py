"""
python -m pytest test/test_issues_and_unreferenced.py 
"""
from pytest import mark


def test_undefined(bf):
    """
    Test for the existence of references to undefined
    configuration construtcts. For instance,
    references to non-existant route-maps.
    """
    df = bf.q.undefinedReferences().answer().frame()
    assert df.empty is True


@mark.batfish_issues
def test_issues(bf):
    """
    Test for the absence of issues detected by
    the checks that ship with Batfish:

    https://batfish.readthedocs.io/en/latest/notebooks/snapshot.html#Snapshot-Initialization-Issues
    """
    df = bf.q.initIssues().answer().frame()
    assert df.empty is True
