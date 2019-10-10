#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
MIMU:
----

Reads MIMU JSON and creates datasets.

"""

import logging
from urllib.parse import  quote_plus

from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
from hdx.data.showcase import Showcase
from slugify import slugify

logger = logging.getLogger(__name__)

tag_mapping = {'Elevation': 'elevation - topography - altitude', 'Boundaries': 'geodata',
               'Location': 'populated places - settlements', 'Transportation': 'transportation',
               'Structure': 'facilities and infrastructure', 'Environment': 'environment',
               'Inland Waters': 'river'}


def get_layersdata(base_url, downloader):
    response = downloader.download('%sapi/layers' % base_url)
    jsonresponse = response.json()
    return jsonresponse['objects']


def generate_dataset_and_showcase(base_url, layerdata):
    """Parse json of the form:
{
"abstract": "Low-lying Areas below 5 meters elevation.",
"category__gn_description": "Elevation",
"csw_type": "dataset",
"csw_wkt_geometry": "POLYGON((92.1729167192825 9.6712496288236,92.1729167192825 21.572916583682,99.1387502212894 21.572916583682,99.1387502212894 9.6712496288236,92.1729167192825 9.6712496288236))",
"date": "2019-08-27T03:09:00",
"detail_url": "/layers/geonode%3Abelow5m_shp",
"distribution_description": "Web address (URL)",
"distribution_url": "http://geonode.themimu.info/layers/geonode%3Abelow5m_shp",
"id": 221,
"owner__username": "MIMU-GIS",
"popular_count": 11,
"rating": 0,
"share_count": 0,
"srid": "EPSG:4326",
"supplemental_information": " This dataset is derived from the Multi-Error-Removed Improved-Terrain / MERIT DEM. ",
"thumbnail_url": "http://geonode.themimu.info/uploaded/thumbs/layer-f70b1880-c8a1-11e9-aea4-42010a80000c-thumb.png",
"title": "Myanmar Low-Lying Areas",
"uuid": "f70b1880-c8a1-11e9-aea4-42010a80000c"
}
    """
    title = layerdata['title']
    logger.info('Creating dataset: %s' % title)
    name = 'MIMU %s' % title
    slugified_name = slugify(name).lower()
    notes = layerdata['abstract']
    dataset = Dataset({
        'name': slugified_name,
        'title': title,
        'notes': '%s\n\n%s' % (notes, layerdata['supplemental_information'])
    })
    dataset.set_maintainer('196196be-6037-4488-8b71-d786adf4c081')
    dataset.set_organization('bde18602-2e92-462a-8e88-a0018a7b13f9')
    dataset.set_dataset_date(layerdata['date'])
    dataset.set_expected_update_frequency('Adhoc')
    dataset.set_subnational(True)
    dataset.add_country_location('mmr')
    tag = layerdata['category__gn_description']
    if tag is None:
        if 'land cover' in notes or 'forest' in notes:  # currently this should cover all null tags
            tag = 'land use and land cover'
    if tag in tag_mapping:
        tag = tag_mapping[tag]
    tags = ['geodata', tag]
    dataset.add_tags(tags)
    srid = quote_plus(layerdata['srid'])
    typename = layerdata['detail_url'].rsplit('/', 1)[-1]
    resource = Resource({
        'name': '%s shapefile' % title,
        'url': '%sgeoserver/wfs?format_options=charset:UTF-8&typename=%s&outputFormat=SHAPE-ZIP&version=1.0.0&service=WFS&request=GetFeature' % (base_url, typename),
        'description': 'Zipped Shapefile. %s' % notes
    })
    resource.set_file_type('zipped shapefile')
    dataset.add_update_resource(resource)
    resource = Resource({
        'name': '%s geojson' % title,
        'url': '%sgeoserver/wfs?srsName=%s&typename=%s&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature' % (base_url, srid, typename),
        'description': 'GeoJSON file. %s' % notes
    })
    resource.set_file_type('GeoJSON')
    dataset.add_update_resource(resource)

    showcase = Showcase({
        'name': '%s-showcase' % slugified_name,
        'title': title,
        'notes': notes,
        'url': layerdata['distribution_url'],
        'image_url': layerdata['thumbnail_url']
    })
    showcase.add_tags(tags)
    return dataset, showcase
