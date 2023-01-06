from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *

# Instantiate a pybatfish session and create a snapshot:
SNAPSHOT_DIR = "snapshots/"
SNAP_SHOT_NAME = "example_snap_new"
SNAP_SHOT_NETWORK_NAME = "example_dc"


bf = Session(host="localhost")
bf.set_network(SNAP_SHOT_NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_DIR, name=SNAP_SHOT_NAME, overwrite=True)
bf.set_snapshot(SNAP_SHOT_NAME)


bgp_process_df = bf.q.bgpProcessConfiguration().answer().frame()

bgp_config_df = bf.q.bgpPeerConfiguration().answer().frame()

node_df = bf.q.nodeProperties().answer().frame()

interface_df = bf.q.interfaceProperties().answer().frame()

named_structures_df = bf.q.namedStructures().answer().frame()
