from abc import ABC
from typing import Any, List, Union

from pandas import Series

from ..model.node_classification_model import NCModel
from ..pipeline.classification_training_pipeline import ClassificationTrainingPipeline
from ..query_runner.query_runner import QueryRunner


class NCTrainingPipeline(ClassificationTrainingPipeline[NCModel], ABC):
    def selectFeatures(self, node_properties: Union[str, List[str]]) -> "Series[Any]":
        """
        Select the node properties to use for training.

        Args:
            node_properties: The node properties to use for training.

        Returns:
            The result of the query.

        """
        query = f"{self._query_prefix()}selectFeatures($pipeline_name, $node_properties)"
        params = {"pipeline_name": self.name(), "node_properties": node_properties}

        return self._query_runner.run_query(query, params).squeeze()  # type: ignore

    def feature_properties(self) -> "Series[Any]":
        """
        Get the feature properties of the pipeline.

        Returns:
            A Series containing the feature properties of the pipeline.

        """
        pipeline_info = self._list_info()["pipelineInfo"][0]
        feature_properties: "Series[Any]" = Series(pipeline_info["featurePipeline"]["featureProperties"], dtype=object)
        return feature_properties

    def _query_prefix(self) -> str:
        return "CALL gds.beta.pipeline.nodeClassification."

    def _create_trained_model(self, name: str, query_runner: QueryRunner) -> NCModel:
        return NCModel(name, query_runner, self._server_version)
