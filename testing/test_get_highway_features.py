"""
This is a stubbed out test file designed to be used with PyTest, but can 
easily be modified to support any testing framework.
"""

from pathlib import Path
import sys

import arcpy

# get paths to useful resources - notably where the src directory is
self_pth = Path(__file__)
dir_test = self_pth.parent
dir_prj = dir_test.parent
dir_src = dir_prj / 'src'

# insert the src directory into the path if not already present
if "get_highway_features" not in sys.modules:
    sys.path.insert(0, str(dir_src))


def test_validate_network_dataset(network_dataset_path):
    """Test the validate_network_dataset function."""
    from get_highway_features.__main__ import validate_network_dataset

    validated_path = validate_network_dataset(network_dataset_path)
    assert validated_path == str(network_dataset_path)


def test_get_network_lines(network_dataset_path):
    """Test the get_network_lines function."""
    from get_highway_features.__main__ import get_network_lines_layer

    lines_layer = get_network_lines_layer(network_dataset_path, edge_type=3)
    assert isinstance(lines_layer, arcpy._mp.Layer)
    assert lines_layer.isFeatureLayer


def test_get_network_lines_feature_set(network_dataset_path):
    """Test retrieving network line features."""
    from get_highway_features.__main__ import get_network_lines_feature_set

    lines_features = get_network_lines_feature_set(network_dataset_path)
    assert isinstance(lines_features, arcpy.FeatureSet)
