"""
Licensing

Copyright 2020 Esri

Licensed under the Apache License, Version 2.0 (the "License"); You
may not use this file except in compliance with the License. You may
obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

A copy of the license is available in the repository's
LICENSE file.
"""
from configparser import ConfigParser
import datetime
from pathlib import Path
import importlib.util
import sys

import arcpy

# path to the root of the project
dir_prj = Path(__file__).parent.parent

# if the project package is not installed in the environment
if importlib.util.find_spec('get_highway_features') is None:
    
    # get the relative path to where the source directory is located
    src_dir = dir_prj / 'src'

    # throw an error if the source directory cannot be located
    if not src_dir.exists():
        raise EnvironmentError('Unable to import get_highway_features.')

    # add the source directory to the paths searched when importing
    sys.path.insert(0, str(src_dir))

# import get_highway_features
from get_highway_features import get_network_line_endpoints, get_network_lines_midpoints
from get_highway_features.utils import get_logger

# read and configure 
config = ConfigParser()
config.read(dir_prj / 'config' / 'config.ini')

log_level = config.get('DEFAULT', 'LOG_LEVEL')
network_dataset_path = config.get('DEFAULT', 'NETWORK_DATASET_PATH')

if __name__ == '__main__':

    # get datestring for file naming yyyymmddThhmmss
    date_string = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

    # path to save log file
    log_dir = dir_prj / 'data' / 'logs'

    if not log_dir.exists():
        log_dir.mkdir(parents=True)

    log_file = log_dir / f'{Path(__file__).stem}_{date_string}.log'

    # use the log level from the config to set up logging
    logger = get_logger(logger_name=f"{Path(__file__).stem}", level=log_level)

    # make sure the output directory and file geodatabase exist
    out_gdb = dir_prj / 'data' / 'processed' / 'processed.gdb'

    # make sure the output directory exists
    out_gdb.parent.mkdir(parents=True, exist_ok=True)

    # make sure the output file geodatabase exists
    if not out_gdb.exists():
        logger.info(f'Creating output file geodatabase: {out_gdb}')
        arcpy.management.CreateFileGDB(str(out_gdb.parent), out_gdb.name)
    else:
        logger.debug(f'Output file geodatabase already exists: {out_gdb}')

    logger.info(f'Starting data processing for {dir_prj.name}')

    # get the network line endpoints
    endpoints_output = str(out_gdb / f'network_line_endpoints_{date_string}')
    logger.info('Retrieving network line endpoints...')
    endpoints_features = get_network_line_endpoints(
        dataset_path=network_dataset_path,
        output_features=endpoints_output
    )
    logger.info(f'Network line endpoints saved to: {endpoints_features}')

    # get the network line midpoints
    midpoints_output = str(out_gdb / f'network_line_midpoints_{date_string}')
    logger.info('Retrieving network line midpoints...')
    midpoints_features = get_network_lines_midpoints(
        dataset_path=network_dataset_path,
        output_features=midpoints_output
    )
    logger.info(f'Network line midpoints saved to: {midpoints_features}')

    # rebuild the spatial indexes on the output feature classes
    for feature_class in [endpoints_features, midpoints_features]:
        logger.info(f'Rebuilding spatial index for: {feature_class}')
        arcpy.management.RebuildIndexes(input_database=feature_class)

    # compress the file geodatabase
    logger.info(f'Compressing file geodatabase: {out_gdb}')
    arcpy.management.Compress(in_dataset=out_gdb)

    logger.info('Data processing complete.')
