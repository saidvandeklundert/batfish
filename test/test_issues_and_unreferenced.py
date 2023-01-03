"""
python -m pytest test/test_issues_and_unreferenced.py 
"""


def test_undefined(bf):
    """
    Test for the existence of references to undefined
    configuration constructs. For instance,
    references to non-existent route-maps.
    """
    df = bf.q.undefinedReferences().answer().frame()
    assert df.empty is True


def test_issues(bf):
    """
    Test for the absence of issues detected by
    the checks that ship with Batfish:

    https://batfish.readthedocs.io/en/latest/notebooks/snapshot.html#Snapshot-Initialization-Issues
    """
    df = bf.q.initIssues().answer().frame()
    assert df.empty is True
