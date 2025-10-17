from typing import Union, Optional
from pathlib import Path

import arcpy

from .utils import get_logger

# configure module logging
logger = get_logger(logger_name="get_highway_features", level="DEBUG")


# get the network dataset
def validate_network_dataset(dataset_path: Union[str, Path]) -> str:
    """
    Get the network dataset from the network dataset path.

    Args:
        dataset_path (Union[str, Path]): Path to the network dataset.

    Returns:
        Path: The validated network dataset path.

    Raises:
        FileNotFoundError: If the dataset path does not exist.
        ValueError: If the provided path is not a network dataset.
        TypeError: If the provided path is not a string or Path object.
    """
    if not isinstance(dataset_path, (str, Path)):
        msg = f"dataset_path must be a string or Path object. Provided type: {type(dataset_path)}"
        logger.error(msg)
        raise TypeError(msg)

    dataset_path = str(dataset_path)

    if not arcpy.Exists(dataset_path):
        msg = f"Network dataset path does not exist: {dataset_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    desc = arcpy.Describe(dataset_path)

    if desc.dataType != "NetworkDataset":
        msg = f"Dataset does not appear to be an ArcPy network dataset: {dataset_path}"
        logger.error(msg)
        raise TypeError(msg)

    logger.debug(f"Network dataset is valid: {dataset_path}")
    return dataset_path


def get_network_lines_layer(
    dataset_path: Union[str, Path], edge_type: Optional[int] = 3
) -> arcpy._mp.Layer:
    """
    Retrieve network lines from the specified network dataset.

    Args:
        dataset_path (Union[str, Path]): Path to the network dataset.
        edge_type (int): Type of network lines to retrieve. Default is 3 (highway ramps).

    Returns:
        arcpy._mp.Layer: The network lines layer.

    Raises:
        ValueError: If the line_type is not valid.
    """
    # ensure the network dataset is valid
    network_dataset_path = validate_network_dataset(dataset_path)

    # describe the network dataset
    desc = arcpy.Describe(network_dataset_path)

    # get the path to the feature dataset containing the network dataset
    feature_dataset_path = Path(network_dataset_path).parent

    # get the edge sources from the network dataset
    edge_sources = desc.edgeSources

    # make sure there is at least one edge source
    if len(edge_sources) == 0:
        msg = f"No edge sources found in network dataset: {network_dataset_path}"
        logger.error(msg)
        raise ValueError(msg)

    # get the edge source feature class
    edge_features_name = edge_sources[0].name

    # create the full path to the edge feature class
    edge_features_path = str(feature_dataset_path / edge_features_name)

    # build the sql query to select edge features by type
    sql_str = f"ROAD_CLASS = {edge_type}"

    # check to see if any features by trying to iterate the first feature
    try:
        next(
            arcpy.da.SearchCursor(
                edge_features_path, field_names="OID@", where_clause=sql_str
            )
        )
    except StopIteration:
        msg = f"No features found in network dataset edges source '{edge_features_path}' with ROAD_CLASS = {edge_type}."
        logger.error(msg)
        raise ValueError(msg)

    # create a feature layer from the edge features
    lyr = arcpy.management.MakeFeatureLayer(
        edge_features_path, out_layer="network_features_lyr", where_clause=sql_str
    )[0]

    logger.debug(
        f"Created layer from network dataset edges source: {edge_features_path}."
    )

    return lyr


def get_network_lines_feature_set(
    dataset_path: Union[str, Path], edge_type: Optional[int] = 3
) -> arcpy.FeatureSet:
    """
    Retrieve network lines from the specified network dataset as a FeatureSet.

    Args:
        dataset_path (Union[str, Path]): Path to the network dataset.
        edge_type (int): Type of network lines to retrieve. Default is 3 (highway ramps).

    Returns:
        arcpy.FeatureSet: The network lines feature set.
    """
    # get the network lines layer
    lines_layer = get_network_lines_layer(dataset_path, edge_type=edge_type)

    # create a feature set from the layer
    feature_set = arcpy.FeatureSet()
    feature_set.load(lines_layer)

    logger.debug("Retrieved network lines as FeatureSet.")

    return feature_set


def get_network_line_endpoints(
    dataset_path: Union[str, Path],
    output_features: Union[str, Path],
    edge_type: Optional[int] = 3,
) -> Path:
    """
    Retrieve the endpoints of network lines from the specified network dataset.

    Args:
        dataset_path (Union[str, Path]): Path to the network dataset.
        output_features (Union[str, Path]): Path to the output feature class.
        edge_type (int): Type of network lines to retrieve. Default is 3 (highway ramps).

    Returns:
        Path: The endpoints feature class.
    """
    # get the network lines layer
    lines = get_network_lines_layer(dataset_path, edge_type=edge_type)

    # create the feature layer for the endpoints
    endpoints_features = arcpy.management.FeatureVerticesToPoints(
        in_features=lines,
        out_feature_class=output_features,
        point_location="BOTH_ENDS",
    )[0]

    logger.debug("Retrieved endpoints of network lines.")

    return Path(endpoints_features)


def get_network_lines_midpoints(
    dataset_path: Union[str, Path],
    output_features: Union[str, Path],
    edge_type: Optional[int] = 3) -> Path:
    """
    Retrieve the midpoints of network lines from the specified network dataset.

    Args:
        dataset_path (Union[str, Path]): Path to the network dataset.
        output_features (Union[str, Path]): Path to the output feature class.
        edge_type (int): Type of network lines to retrieve. Default is 3 (highway ramps).
    """
    # get the network lines layer
    lines = get_network_lines_feature_set(dataset_path, edge_type=edge_type)

    # create the feature layer for the midpoints
    midpoints_features = arcpy.management.FeatureVerticesToPoints(
        in_features=lines,
        out_feature_class=output_features,
        point_location="MID",
    )[0]

    logger.debug("Retrieved midpoints of network lines.")

    return Path(midpoints_features)
