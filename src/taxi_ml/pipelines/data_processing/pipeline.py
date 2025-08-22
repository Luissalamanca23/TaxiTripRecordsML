"""
Data processing pipeline for NYC Taxi ML project.
"""

from kedro.pipeline import Node, Pipeline

from .nodes import preprocess_taxi_data, split_data


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        Node(
            func=preprocess_taxi_data,
            inputs="taxi_raw",
            outputs="taxi_processed",
            name="preprocess_taxi_data_node",
        ),
        Node(
            func=split_data,
            inputs="taxi_processed", 
            outputs=["taxi_train", "taxi_val", "taxi_test"],
            name="split_data_node",
        ),
    ])
