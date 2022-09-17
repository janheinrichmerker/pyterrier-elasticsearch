from logging import basicConfig, Logger, getLogger

from importlib_metadata import version

from pyterrier_elasticsearch import retrieve

__version__ = version("pyterrier_elasticsearch")

basicConfig()
logger: Logger = getLogger("pyterrier_elasticsearch")

# Re-export from child modules.
ElasticsearchRetrieve = retrieve.ElasticsearchRetrieve
