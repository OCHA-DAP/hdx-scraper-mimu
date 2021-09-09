#!/usr/bin/python
"""
Top level script. Calls other functions that generate datasets that this script then creates in HDX.

"""
import logging
import re
from os.path import expanduser, join

from hdx.facades.simple import facade
from hdx.hdx_configuration import Configuration
from hdx.scraper.geonode.geonodetohdx import GeoNodeToHDX
from hdx.utilities.downloader import Download
from hdx.utilities.text import remove_string

logger = logging.getLogger(__name__)

lookup = "hdx-scraper-mimu"
VERSION_PATTERN = re.compile(r"[\-\s_]v\d*(-\d*)+")


def process_dataset_name(name):
    match = VERSION_PATTERN.search(name)
    if match is not None:
        name = remove_string(name, match.group(0))
    return name


def create_dataset_showcase(dataset, showcase, **kwargs):
    logger.info(f"Dataset date is {dataset['dataset_date']}")


def main():
    """Generate dataset and create it in HDX"""

    with Download() as downloader:
        configuration = Configuration.read()
        base_url = configuration["base_url"]
        dataset_tags_mapping = configuration["dataset_tags_mapping"]
        geonodetohdx = GeoNodeToHDX(base_url, downloader)
        countrydata = {"iso3": "MMR", "name": "Myanmar", "layers": None}
        metadata = {
            "maintainerid": "196196be-6037-4488-8b71-d786adf4c081",
            "orgid": "bde18602-2e92-462a-8e88-a0018a7b13f9",
        }

        datasets = geonodetohdx.generate_datasets_and_showcases(
            metadata,
            countrydata=countrydata,
            get_date_from_title=True,
            process_dataset_name=process_dataset_name,
            dataset_tags_mapping=dataset_tags_mapping,
            updated_by_script="HDX Scraper: MIMU GeoNode",
        )
        geonodetohdx.delete_other_datasets(datasets, metadata)


if __name__ == "__main__":
    facade(
        main,
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup=lookup,
        project_config_yaml=join("config", "project_configuration.yml"),
    )
