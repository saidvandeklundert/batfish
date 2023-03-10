import pytest
import pandas as pd
import pybatfish
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *


SNAPSHOT_DIR = "snapshots/"
SNAP_SHOT_NAME = "example_snap_new"
SNAP_SHOT_NETWORK_NAME = "example_dc"


@pytest.fixture(scope="session")
def bf() -> pybatfish.client.session.Session:
    """returns a BatFish session for reuse throughtout the tests."""
    bf = Session(host="localhost")
    bf.set_network(SNAP_SHOT_NETWORK_NAME)
    bf.init_snapshot(SNAPSHOT_DIR, name=SNAP_SHOT_NAME, overwrite=True)
    bf.set_snapshot(SNAP_SHOT_NAME)
    return bf


@pytest.fixture(scope="session")
def bgp_process_configuration(bf) -> pd.DataFrame:
    df = bf.q.bgpProcessConfiguration().answer().frame()
    return df


@pytest.fixture(scope="session")
def bgp_peer_configuration(bf) -> pd.DataFrame:
    df = bf.q.bgpPeerConfiguration().answer().frame()
    return df


@pytest.fixture(scope="session")
def different_as(bgp_peer_configuration):
    """Dataframe with peers residing in different autonomous systems."""
    diff_as = bgp_peer_configuration["Local_AS"] != bgp_peer_configuration[
        "Remote_AS"
    ].astype(int)
    return bgp_peer_configuration[diff_as]


@pytest.fixture(scope="session")
def node_properties(bf) -> pd.DataFrame:
    df = bf.q.nodeProperties().answer().frame()
    return df


@pytest.fixture(scope="session")
def all_nodes(node_properties):
    return list(node_properties["Node"])


@pytest.fixture(scope="session")
def interface_properties(bf) -> pd.DataFrame:
    df = bf.q.interfaceProperties().answer().frame()
    return df


@pytest.fixture(scope="session")
def named_structures(bf) -> pd.DataFrame:
    df = bf.q.namedStructures().answer().frame()
    return df
