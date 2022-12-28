# Batfish testing pipeline

Example pipeline for Batfish


## Quickstart

Start the container with the batfish service:

```
docker pull batfish/allinone
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone
```

Setup the Python stuff:
```
python -m pipenv check
python -m pipenv update
python -m pipenv shell
# 'exit' to leave the pipenv shell
```

To run the tests:
```
python -m pytest .
python -m pytest . -W ignore::DeprecationWarning
```




## Notes:

This example pipeline uses configurations found in the Batfish repo, [here](https://github.com/batfish/batfish/tree/master/networks). Certain snippets of config were added to trigger some tests to pass/fail.