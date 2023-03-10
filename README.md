## Quickstart: Batfish up and running in 5 minutes

Start the container with the batfish service:

```
docker pull batfish/allinone
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone
```

Install the relevant Python dependencies :

```
python -m pipenv check
python -m pipenv update
python -m pipenv shell
```

Run all tests located in the `test` directory:

```
python -m pytest
```

Run specific tests:
```
pytest test/test_firewall_filters.py::test_should_be_allowed
```

Run test and drop to the debugger when the test fails:
```
pytest -vvvv test/test_firewall_filters.py::test_should_be_allowed --pdb
```

Play with the service in ipython:

```python
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *

SNAPSHOT_DIR = "snapshots/"
SNAP_SHOT_NAME = "example_snap_new"
SNAP_SHOT_NETWORK_NAME = "example_dc"


bf = Session(host="localhost")
bf.set_network(SNAP_SHOT_NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_DIR, name=SNAP_SHOT_NAME, overwrite=True)
bf.set_snapshot(SNAP_SHOT_NAME)

bf.q.initIssues().answer().frame()
bf.q.undefinedReferences().answer().frame()

bf.q.interfaceProperties().answer().frame()
```

Goes with [this](https://saidvandeklundert.net/2023-01-05-batfish/) post.

## Notes:

This example uses configurations found in the Batfish repo, [here](https://github.com/batfish/batfish/tree/master/networks). I am using them with permission. Certain snippets of config were added to trigger some tests to pass/fail.

The configurations were added simply to have _something_ to work on. The idea is that users replace the configurations with their own and then tweak the tests.