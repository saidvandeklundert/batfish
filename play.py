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

# Interfaces:
df = bf.q.interfaceProperties().answer().frame()

# check for deviating MTU:
mtu_std = df["MTU"] == 1500
interfaces_with_deviating_mtu = df[~mtu_std][["Interface", "MTU"]]
interfaces_with_deviating_mtu.empty

# check for deviating MTU:
small_mtu = df["MTU"] < 1500
big_mtu = df["MTU"] > 1500
df[small_mtu | big_mtu]

# find all interfaces with MTU of 1800:
mtu_1800 = df["MTU"] == 1800
df[mtu_1800]
df[mtu_1800]["Description"]
df[mtu_1800].empty

# Check descriptions:
has_description = df["Description"].notnull()
df[has_description]
df[has_description][["Interface", "Description", "Admin_Up"]]
# Check UNUSED description:
unused = df["Description"] == "UNUSED"
df[unused][["Interface", "Description", "Admin_Up"]]

# Non-default vrf:
non_default_vrf = df["VRF"] != "default"
df[non_default_vrf]

# iterate the Pandas dataframe:
for index, row in df.iterrows():
    print(index)
    print(row)
    print(row["Interface"])
    print(row["Interface"].hostname)
    print(type(row["Interface"]))

for row in df.itertuples():
    print(row)
    print(row[1])
    print(row["Interface"])
    print(row["Interface"].hostname)
    print(type(row["Interface"]))


for index, row in df.iterrows():
    if row["Description"]:
        print(index)
        print(row)
        print(row["Description"])
        print(type(row["Description"]))
        x = row["Description"]

df[unused]
df[unused][["Interface", "Description", "Admin_Up"]]


unused = df["Description"].str.contains("UNUSED", na=False)
admin_up = df["Admin_Up"] == True
unused_and_up = df[unused & admin_up]
