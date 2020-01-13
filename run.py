#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Top level script. Calls other functions that generate datasets that this script then creates in HDX.

"""
import logging
import re
from os.path import join, expanduser

from hdx.hdx_configuration import Configuration
from hdx.scraper.geonode.geonodetohdx import GeoNodeToHDX
from hdx.utilities.downloader import Download

from hdx.facades.simple import facade

logger = logging.getLogger(__name__)

lookup = 'hdx-scraper-mimu'
VERSION_PATTERN = re.compile('[\-\s_]v\d*(-\d*)+')


def process_dataset_name(name):
    match = VERSION_PATTERN.search(name)
    if match is not None:
        name = GeoNodeToHDX.remove(name, match.group(0))
    return name


def create_dataset_showcase(dataset, showcase):
    logger.info('Dataset date is %s' % dataset['dataset_date'])


def main():
    """Generate dataset and create it in HDX"""

    with Download() as downloader:
        base_url = Configuration.read()['base_url']
        geonodetohdx = GeoNodeToHDX(base_url, downloader)
        countrydata = {'iso3': 'MMR', 'name': 'Myanmar', 'layers': None}
        datasets = geonodetohdx.generate_datasets_and_showcases('196196be-6037-4488-8b71-d786adf4c081',
                                                                'bde18602-2e92-462a-8e88-a0018a7b13f9', 'MIMU',
                                                                countrydata=countrydata, get_date_from_title=True,
                                                                process_dataset_name=process_dataset_name)
#                                                                create_dataset_showcase=create_dataset_showcase)
        geonodetohdx.delete_other_datasets(datasets)


if __name__ == '__main__':
    facade(main, user_agent_config_yaml=join(expanduser('~'), '.useragents.yml'), user_agent_lookup=lookup, project_config_yaml=join('config', 'project_configuration.yml'))


