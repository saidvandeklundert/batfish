# Testing network configuration using Batfish, Pandas and pytest

Examples on how to test and validate network configurations leveraging Batfish, Pandas and pytest.

![Batfish](/img/batfish.png)

More on Batfish, Pandas and pytest will follow soon.

## What is Batfish

Batfish according to [Batfish](https://github.com/batfish/batfish):
```
Batfish is a network validation tool that provides correctness guarantees for security, reliability, and compliance by analyzing the configuration of network devices. It builds complete models of network behavior from device configurations and finds violations of network policies (built-in, user-defined, and best-practices).
```

The two main components to Batfish are the following:
- Batfish service: the software that analyzes the configurations
- Batfish client: the `pybatfish` Python client that allows users to interact with the Batfish service.

Typically, I think, the Batfish service is run in a container. The Batfish client feeds the service with all the required input data: 

![Batfish overview](/img/batfish_client_service_parse.png)

As shown above, the Batfish client is used to upload all relevant configurations. This is significant because it allows Batfish to operate without network device access, making it easy to integrate into the suite of automation tools in place and allowing it to operate on configurations prior to their actual deployment.

After recieving the configurations, the service runs parses the data and produces the models. When this is completed, the client can start asking the service questions in order to retrieve a variety datamodels.

The first thing of interest is the `initIssues` questions that Batfish offers. This 'out of the box' questions can detect several configuration issues for you. The second thing worth noting is `undefinedReferences`, which will notify you in case one of your configuration constructs (like a route-map) references something that does not exist (an access-list for instance).

However, the real treasure trove is the models that the Batfish service builds for you based on the configurations you provide. You can access these models through a variety of questions. The methods that allow you to ask these questions can be made to return a Pandas dataframe. These models can be put to good use in different scenario's:
- making assertions during CI to verify the state of the network configuration prior to deploying the configurations
- feeding the data models to other (micro-)services to enhance their insights into the network. For instance:
  - have the monitoring system better understand what constructs exist and should be monitored (BGP sessions for instance)
  - feed the models into a service that exposes the models for other applications to consume
  - etc.
- making assertions against different snapshots for pre- and post-change validations

## Your first snapshot:

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
```


## Pandas

Many blogs and books have been written about Pandas and there is a lot to learn and discover about the framework. However, in the context of Batfish, there is a lot you can get done knowing just some of the basics. First, I'll discuss the most important datastructure in Pandas and after that, I will share some recipes that I turned to most often.

The datastructure that is used to deliver all the goodness that Batfish has to offer is the Pandas Dataframe.

![Pandas Dataframe](/img/pandas_dataframe.png)

`Dataframe`: 2-dimensional data structure that can store different types of data. The Dataframe consists of columns and rows. Every column in a DataFrame is a `Series`.


`Series`: a one-dimensional labeled array capable of holding any data stype. The axis labels are referred to as the `index`. The `Series` represent a single column in a dataframe.


###


df.columns  # check column names
df.iloc[0]  # integer-location based indexing for selection by position
df.head(6)  # first 6 rows of the frame
df.tail(6)  # last 6 rows of the frame

```
In [17]: df.tail(6)
Out[17]: 
          Node      VRF Local_AS    Local_IP Local_Interface Confederation  ... Cluster_ID Peer_Group   Import_Policy   Export_Policy Send_Community Is_Passive     
31    as2dist1  default        2     2.1.3.1            None          None  ...       None        as2              []              []           True      False     
32    as2dist2  default        2     2.1.3.2            None          None  ...       None        as2              []              []           True      False     
33    as2dist2  default        2     2.1.3.2            None          None  ...       None        as2              []              []           True      False     
34  as1border2  default        1  10.14.22.1            None          None  ...       None        as4  ['as4_to_as1']  ['as1_to_as4']          False      False     
35    as1core1  default        1    1.10.1.1            None          None  ...   1.10.1.1        as1              []              []           True      False     
36  as1border2  default        1     1.2.2.2            None          None  ...       None        as1              []              []           True      False     
```

### Filtering and selecting values of interest

### Iterating the Pandas dataframe

### Converting the Pandas Dataframe to another datastructure


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
# 'exit' to leave the pipenv shell
```

Run all tests located in the `test` directory:

```
python -m pytest
```




## Interesting links:

[Batfish documentation](https://batfish.readthedocs.io/en/latest/)
[Batfish questions](https://batfish.readthedocs.io/en/latest/questions.html)
[Datamodels in the pybatfish repo](https://github.com/batfish/pybatfish/blob/master/pybatfish/datamodel)

[Batfish asserts source code](https://github.com/batfish/pybatfish/blob/master/pybatfish/client/asserts.py)

[Pandas tutorials](http://pandas.pydata.org/docs/getting_started/intro_tutorials/)


https://github.com/saidvandeklundert/batfish

## Notes:

This example blog uses configurations found in the Batfish repo, [here](https://github.com/batfish/batfish/tree/master/networks). I am using them with permission. Certain snippets of config were added to trigger some tests to pass/fail.