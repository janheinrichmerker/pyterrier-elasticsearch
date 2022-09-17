from dataclasses import dataclass
from itertools import islice
from typing import Optional, Any, Dict, NamedTuple, Mapping, Collection

from elasticsearch import Elasticsearch
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy
from pyterrier.batchretrieve import BatchRetrieveBase
from pyterrier.model import add_ranks
from tqdm.auto import tqdm


class _Result(NamedTuple):
    id: str
    score: float
    source: Dict[str, Any]


@dataclass
class ElasticsearchRetrieve(BatchRetrieveBase):
    name = "ElasticsearchRetrieve"

    client: Elasticsearch
    index: str
    fields: Collection[str]
    columns: Optional[Mapping[str, str]] = None
    num_results: Optional[int] = 10
    verbose: bool = False

    @classmethod
    def connect(
            cls,
            index: str,
            fields: Collection[str],
            columns: Optional[Mapping[str, str]] = None,
            num_results: Optional[int] = 10,
            verbose: bool = False,
            **kwargs,
    ) -> "ElasticsearchRetrieve":
        if columns is None:
            columns = {}
        return ElasticsearchRetrieve(
            client=Elasticsearch(**kwargs),
            index=index,
            fields=fields,
            columns=columns,
            num_results=num_results,
            verbose=verbose,
        )

    @property
    def _columns(self) -> Mapping[str, str]:
        if self.columns is None:
            return {field: field for field in self.fields}
        else:
            return self.columns

    def __post_init__(self):
        super().__init__(verbose=self.verbose)

    def _merge_result(
            self,
            row: Dict[str, Any],
            result: _Result
    ) -> Dict[str, Any]:
        row = {
            **row,
            "docno": result.id,
            "score": result.score,
        }
        for path, dest in self.columns.items():
            value = result.source
            for component in path.split("."):
                value = value[component]
            row["dest"] = value
        return row

    def _transform_query(self, topic: DataFrame) -> DataFrame:
        if len(topic.index) != 1:
            raise RuntimeError("Can only transform one query at a time.")

        row: Dict[str, Any] = topic.to_dict(orient="records")[0]
        query: str = row["query"]

        response = self.client.search(
            index=self.index,
            track_total_hits=False,
            query={
                "multi_match": {
                    "query": query,
                    "fields": list(self.fields),
                }
            },
            size=self.num_results
        )
        results = (
            _Result(
                hit["_id"],
                float(hit["_score"]),
                hit["_source"]
            )
            for hit in response['hits']['hits']
        )
        if self.num_results is not None:
            results = islice(results, self.num_results)

        return DataFrame([
            self._merge_result(row, result)
            for result in results
        ])

    def transform(self, topics: DataFrame) -> DataFrame:

        if not isinstance(topics, DataFrame):
            raise RuntimeError("Can only transform dataframes.")

        if not {'qid', 'query'}.issubset(topics.columns):
            raise RuntimeError("Needs qid and query columns.")

        if len(topics) == 0:
            return self._transform_query(topics)

        topics_by_query: DataFrameGroupBy = topics.groupby(
            by=["qid"],
            as_index=False,
            sort=False,
        )
        if self.verbose:
            # Show p/home/heinrich/Repositories/pyterrier-elasticsearchrogress during reranking queries.
            tqdm.pandas(
                desc="Searching with Elasticsearch",
                unit="query",
            )
            topics_by_query = topics_by_query.progress_apply(
                self._transform_query
            )
        else:
            topics_by_query = topics_by_query.apply(self._transform_query)

        retrieved: DataFrame = topics_by_query.reset_index(drop=True)
        retrieved.sort_values(by=["score"], ascending=False)
        retrieved = add_ranks(retrieved)

        return retrieved

    def __hash__(self):
        """
        Implement hash function to be able
        to cache pipeline results in PyTerrier.
        """
        return hash((
            repr(self.client),
            repr(self.client.info()),
            self.index,
            self.num_results,
            self.verbose,
        ))
