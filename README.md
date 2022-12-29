# Batfish testing pipeline

Example pipeline for Batfish

![Batfish](/img/batfish.png)

More on Batfish, Pandas and pytest will follow soon.

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

Datamodels in the pybatfish repo: https://github.com/batfish/pybatfish/blob/master/pybatfish/datamodel

Asserts source code: https://github.com/batfish/pybatfish/blob/master/pybatfish/client/asserts.py

## Notes:

This example pipeline uses configurations found in the Batfish repo, [here](https://github.com/batfish/batfish/tree/master/networks). Certain snippets of config were added to trigger some tests to pass/fail.