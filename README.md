[![PyPi](https://img.shields.io/pypi/v/pyterrier_elasticsearch?style=flat-square)](https://pypi.org/project/pyterrier_elasticsearch/)
[![CI](https://img.shields.io/github/workflow/status/heinrichreimer/pyterrier_elasticsearch/CI?style=flat-square)](https://github.com/heinrichreimer/pyterrier_elasticsearch/actions?query=workflow%3A"CI")
[![Code coverage](https://img.shields.io/codecov/c/github/heinrichreimer/pyterrier_elasticsearch?style=flat-square)](https://codecov.io/github/heinrichreimer/pyterrier_elasticsearch/)
[![Python](https://img.shields.io/pypi/pyversions/pyterrier_elasticsearch?style=flat-square)](https://pypi.org/project/pyterrier_elasticsearch/)
[![Issues](https://img.shields.io/github/issues/heinrichreimer/pyterrier_elasticsearch?style=flat-square)](https://github.com/heinrichreimer/pyterrier_elasticsearch/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/heinrichreimer/pyterrier_elasticsearch?style=flat-square)](https://github.com/heinrichreimer/pyterrier_elasticsearch/commits)
[![Downloads](https://img.shields.io/pypi/dm/pyterrier_elasticsearch?style=flat-square)](https://pypi.org/project/pyterrier_elasticsearch/)
[![License](https://img.shields.io/github/license/heinrichreimer/pyterrier_elasticsearch?style=flat-square)](LICENSE)

# 🔍 pyterrier_elasticsearch

Retrieve from Elasticsearch indices in PyTerrier.
Powered by the [`elasticsearch`](https://pypi.org/project/elasticsearch/) package.

## Installation

```shell
pip install pyterrier_elasticsearch
```

## Usage

```python
from elasticsearch import Elasticsearch
from pyterrier_elasticsearch import ElasticsearchRetrieve

client = Elasticsearch(...)
chatnoir = ElasticsearchRetrieve(
    client=client,
    index="test-index",
    fields=["text", "title"],
    columns={
        # source field -> destination column
        "text": "text",
        "title": "title",
    },
)

# Use PyTerrier functions like with BatchRetrieve.
chatnoir.search("python library")
```

Also, check out the [sample notebook](examples/search.ipynb)
or [open it in Google Colab](https://colab.research.google.com/github/heinrichreimer/pyterrier_elasticsearch/blob/main/examples/search.ipynb)
.

## Development

To build and develop this package you need to install the `build` package:

```shell
pip install build
```

### Installation

Install package dependencies:

```shell
pip install -e .
```

### Testing

Install test dependencies:

```shell
pip install -e .[test]
```

Verify your changes against the test suite to verify.

```shell
flake8 pyterrier_elasticsearch examples tests
pylint -E pyterrier_elasticsearch examples tests
pytest pyterrier_elasticsearch examples tests
```

Please also add tests for the axioms or integrations you've added.

### Build wheel

A wheel for this package can be built by:

```shell
python -m build
```

## License

This repository is released under the [MIT license](LICENSE).
