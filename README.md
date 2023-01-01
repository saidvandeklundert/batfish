# Testing network configuration using Batfish, Pandas and pytest

Recently, I started looking into testing and validating network configurations leveraging Batfish, Pandas and pytest. Doing something with Batfish has been on my to-do list for quite a while. After playing with it, I can say it is a real pitty I did not start using this tool earler. 

![Batfish](/img/batfish.png)

This article aims to give people interested in using Batfish as part of their CI a running start by explaining the basics of Batfish and getting it up and running. After this, I will go over bit of Pandas so you can work with the data that is produced by Batfish and I will finish up writing some unit tests using pytest. There will be no mention of any CI tool or deployment method.

## Batfish overview


The 'why' Batfish according to [Batfish](https://github.com/batfish/batfish):

_Batfish is a network validation tool that provides correctness guarantees for security, reliability, and compliance by analyzing the configuration of network devices. It builds complete models of network behavior from device configurations and finds violations of network policies (built-in, user-defined, and best-practices)._

The idea is to analyze the configurations _before_ deploying them. So after your automation generates configuration files or changes, you can use Batfish as a mechanism to provide additional 'correctness guarantees'. In addition to this, there are also other ways in which Batfish can be helpful, more on that later.

### Batfish components 

The two main components to Batfish are the following:
- Batfish service: the software that analyzes the configurations
- Batfish client: the `pybatfish` Python client that allows users to interact with the Batfish service.

Typically, the Batfish service is run in a container and the Batfish client feeds the service with all the required input data: 

![Batfish overview](/img/batfish_client_service_parse.png)

The Batfish client is used to upload all relevant configurations. This allows Batfish to operate without network device access, making it easy to integrate into the suite of automation tools in place and allowing it to operate on configurations prior to their actual deployment.

After recieving the configurations, the service parses the data that was supplied (the configurations) and produces the models. When this is completed, users can start using the client to ask the service 'questions'. When the client is used to ask a question, the service will generate and return an answer that ends up as a Pandas DataFrame for the user to work with.

### Batfish questions

Some questions will return issues found in the configurations and other questions will return a variety of datamodels that describe the network.

The first thing of interest is the `initIssues` questions that Batfish offers. These 'out of the box' questions can detect several configuration issues for you. The second thing worth noting is `undefinedReferences`, which will notify you in case one of your configuration constructs (like a route-map) references something that does not exist (an access-list for instance).

However, the real treasure trove is the models that the Batfish service builds for you based on the configurations you provide. You can access these models through a variety of questions. The methods that allow you to ask these questions can be made to return a Pandas dataframe. These models can be put to good use in different scenario's:
- making assertions during CI to verify the state of the network configuration prior to deploying the configurations
- feeding the data models to other (micro-)services to enhance their insights into the network. For instance:
  - have the monitoring system better understand what constructs exist and should be monitored (BGP sessions for instance)
  - feed the models into a service that exposes the models for other applications to consume
  - etc.
- making assertions against different snapshots for pre- and post-change validations

### Your first snapshot:

Start the container with the batfish service:

```
docker pull batfish/allinone
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone
```

Install the relevant Python dependencies (using [pipenv](https://pypi.org/project/pipenv/) in this example):

```
git clone https://github.com/saidvandeklundert/batfish.git
cd batfish
python -m pipenv check
python -m pipenv update
python -m pipenv shell
```

We have the Batfish service running and we have the proper client software installed. From the same directory, we can start an `ipython` session and run the following:

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

The `bf` variable is a pybatfish client session that is used for all further interactions with the service. To see some data appear on screen, issue the following:

```
bf.q.initIssues().answer().frame()
bf.q.undefinedReferences().answer().frame()
bf.q.interfaceProperties().answer().frame()
```

This will inform you of any issues detected by Batfish, any undefined references in you configuration and it will give you data that describes the interfaces in your network.

The data is delivered in a Pandas DataFrame.

## Pandas

Many blogs and books have been written about Pandas and there is a lot to learn and discover about the framework. However, in the context of Batfish, there is a lot you can get done knowing just some of the basics. First, I'll discuss the most important datastructure in Pandas and after that, I will share some recipes that I turned to most often.

The datastructure that is used to deliver all the goodness that Batfish has to offer is the Pandas Dataframe.

![Pandas Dataframe](/img/pandas_dataframe.png)

`Dataframe`: 2-dimensional data structure that can store different types of data. The Dataframe consists of columns and rows. Every column in a DataFrame is a `Series`.


`Series`: a one-dimensional labeled array capable of holding any data stype. The axis labels are referred to as the `index`. The `Series` represent a single column in a dataframe.


### Basic Pandas operations

The best way to get started with Pandas is by using the basic operations in REPL. Start `ipython` and grab a DataFrame using one of the Batfish questions, for instance `df = bf.q.interfaceProperties().answer().frame()` to work with interface data. After this, explore the dataset with the following:

```
df.columns    # check column names
df.iloc[0]    # integer-location based indexing for selection by position
df.iloc[0:3]  # slice of a DataFrame

df.head(6)    # first 6 rows of the frame
df.tail(6)    # last 6 rows of the frame
df["Node"]    # select 1 row / Series (returns a Series)
df[["Interface","Incoming_Filter_Name",]]    # select multiple rows / Series (returns a DataFrame)
df.iloc[0:3,[1,2]]  # slice of a DataFrame, selecting columns 1 and 2
df.loc[0:10,["Interface","Active"]]  # slice of the DataFrame selecting columns by name

df.to_csv("data.csv")                 # store data as CSV
from_csv = pd.read_csv("data.csv")    # read DataFrame from CSV
```



Note about iloc and loc: with iloc, the row and the columns are selected using an integer to specify the index number of the row/column. With loc, you supply the label of the row/column name. In case the rows are labeled with integers, as is the case with Batfish models, you can select the rows using integers and the columns using their name. Generally, when working with Pybatfish, this is an easier approach.




### Filtering and selecting values of interest

To use the data Batfish has on offer effectively, you need to be able to filter it to find the things that are relevant to your network. Pandas has put a lot of developer ergonomics in place to sift through and filter data. All of these examples were run against the dataframe obtained using `df = bf.q.interfaceProperties().answer().frame()`.

```
# display rows where the MTU is 1500:
df[df["MTU"] == 1500]

# put the selection criteria in a separate variable and then apply it to the DF:
mtu_1500 = df["MTU"] == 1500
df[mtu_1500]

# find interfaces that do NOT have an MTU of 1500:
df[~mtu_1500]
df[~mtu_1500][["Interface","MTU"]]

# alternative approach to finding interfaces that do NOT have an MTU of 1500:
small_mtu = df["MTU"] < 1500
big_mtu = df["MTU"] > 1500
df[small_mtu | big_mtu]

# find interfaces with UNUSED in the description:
# 'na=False' set cells that do not contain "UNUSED" to False
unused = df["Description"].str.contains("UNUSED", na=False)
df[unused]

# we can also do a case-insensitive search:
df["Description"].str.contains("UnUsEd", case=False, na=False)

# search for multiple values:
df["Description"].str.contains("UnUsEd|core", case=False, na=False)

# or apply a regex:
df["Description"].str.contains("U[a-z]u.*d", case=False, na=False, regex=True)


# find admin up interfaces:
admin_up = df["Admin_Up"] == True
df[admin_up]

# find admin up AND unused:
df[unused & admin_up]

```

In case a cell contains something like a string or an integer, applying a comparison operator to it is relatively straightforward. Filtering on cells that contain a composite type can be a bit trickier. I am talking about the difference in types between, for instance, the "Description" and "Interface" columns:

```python
type(df["Description"].iloc[0])
>>>  str

type(df["Interface"].iloc[0])
>>> pybatfish.datamodel.primitives.Interface
vars(df["Interface"].iloc[0])
>>> {'hostname': 'as1border1', 'interface': 'Ethernet0/0'}
```

Filtering rows for conditions applied to the hostname of interface field can be done using a Lambda:

```python
df[
    df.apply(
        lambda row: "core" in row["Interface"].hostname,
        axis=1,  # this applies the function to each row, use 0 to select column
    )
]
```

We are free to add additional logic to the Lambda and add criteria to filter based on other columns as well:
```
df[
    df.apply(
        lambda row: "core" in row["Interface"].hostname
        and row["MTU"] != 1500,
        axis=1,
    )
]

df[
    df.apply(
        lambda row: "core" in row["Interface"].hostname
        and row["MTU"] != 1500
        and row["Active"],
        axis=1,
    )
]
```

Lastly, for certain scenario's, knowing you can iterate the DataFrame might also come in handy:

```
for idx, row in df.iterrows():
  print(idx)
  print(row["Interface"])
  print(row["MTU"])
```

## Pytest

Pytest according to pytest:

_The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries._

Working with Pytest is a joy to me due to the simplicity of the framework and the fact that there are a lot of features in pytest that can make your life easy. There is a fantastic book on the framework which I can really recommend as it will guide you through the most usefull and important features of the framework:

![Pytest book](/img/pytest_book.png)


In the context of using Batfish to test the network, I am going to keep it simple and straightforward. I will mainly let pytest drive the execution of the tests making use of a small amount of features pytest has on offer. 

First, I will show you how to run the tests, then I will discuss fixtures and after that, I will cover some example tests.

### Running the tests

The repo that comes with this article has a directory where all the tests are located. Additionally, there is a `pytest.ini` file containing the pytest configuration. To run all the tests, simply run `pytest` or `python -m pytest` from the top level directory of the repository.

Pytest will then:
- read the configuration options
- look for tests in the test directory
- identify all test functions (functions prefixed with `test_` in their name)
- execute all the tests
- report the results of the tests


### Setting up a fixture

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
[pybatfish examples](https://github.com/batfish/pybatfish/tree/master/jupyter_notebooks)
[Datamodels in the pybatfish repo](https://github.com/batfish/pybatfish/blob/master/pybatfish/datamodel)

[Batfish asserts source code](https://github.com/batfish/pybatfish/blob/master/pybatfish/client/asserts.py)

[Pandas tutorials](http://pandas.pydata.org/docs/getting_started/intro_tutorials/)

[Python Testing with pytest](https://a.co/d/1B1Ryh5)


https://github.com/saidvandeklundert/batfish

## Notes:

This example blog uses configurations found in the Batfish repo, [here](https://github.com/batfish/batfish/tree/master/networks). I am using them with permission. Certain snippets of config were added to trigger some tests to pass/fail.