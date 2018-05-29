import configparser
import argparse
import sys
import requests
from ckanapi import RemoteCKAN
import json
import urllib

config = configparser.ConfigParser()
config.read('config.ini')
ckan_server_URL = config['CKAN']['ckan_server_URL']
ckan_api_key = config['CKAN']['ckan_api_key']

dataset_organization = {
    'name': 'organization-for-tests',
    'display_name': 'Organization For Tests',
    'description': 'Organization for Testing Purposes'
}
dataset_dict = {
    'name': 'data-sample-csv',
    'notes': 'A long description of my dataset',
    'owner_org': 'organization-for-tests',
    'organization': 'organization-for-tests',
    'license_title': 'Creative Commons Attribution',
    'private': 'false',
    "maintainer": "Georg Hagmann",
    "maintainer_email": "georg.hagmann@tuwien.ac.at",
    "author": "Georg Hagmann",
    "author_email": "georg.hagmann@tuwien.ac.at",
    "version": "1.0",
    "license_id": "cc-by",
    "notes": "A generated CSV-Dataset with nonsensical information ",
    "license_url": "http://www.opendefinition.org/licenses/cc-by",
    "title": "Data Sample CSV",
}


mysite = RemoteCKAN(ckan_server_URL, apikey=ckan_api_key)

#mysite.call_action('organization_create', dataset_organization)

mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='data-sample-csv',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='2017-01-sample.csv',
    description = 'Generated nonsensical data',
    upload=open('./RepositoryContents/2017-01-sample.csv', 'rb'))

dataset_dict['name'] = 'data-sample-2-csv'
dataset_dict['notes'] = 'CSV generated in DPUE Task 1'
dataset_dict["url"] =  "https://github.com/alexrashed/tu-dpue-lab1-ss18/blob/master/output/data.csv"
dataset_dict['title'] = "Data Sample 2 CSV"
mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='data-sample-2-csv',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='data.csv',
    description = 'Generated Dataset from DPUE Task 1',
    upload=open('./RepositoryContents/data.csv', 'rb'))

dataset_dict.pop("url")
dataset_dict['name'] = "license-selector-screenshot"
dataset_dict['notes'] = "A screenshot of the License-Selector"
dataset_dict['title'] = "License Selector Screenshot"

mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='license-selector-screenshot',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='6.png',
    description = 'Screenshot of License Selector',
    upload=open('./RepositoryContents/6.png', 'rb'))

dataset_dict['name'] = "students-graphic"
dataset_dict['notes'] = "A Graphic comparing student enrollments in Germany and Austria"
dataset_dict['title'] = "Students Graphic"

mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='students-graphic',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='students.png',
    description = 'A Graphic comparing student enrollments in Germany and Austria.',
    upload=open('./RepositoryContents/students.png', 'rb'))
dataset_dict['name'] = "coding-sample-1"
dataset_dict['notes'] = "Coding Sample from DPUE 1.2"
dataset_dict['title'] = "Coding Sample 1"
dataset_dict['url'] = "https://github.com/alexrashed/tu-dpue-lab2-ss18/blob/master/src/app/app.component.ts"

mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='coding-sample-1',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='app.component.ts',
    description = 'Main class of DPUE Project 1.',
    upload=open('./RepositoryContents/app.component.ts', 'rb'))
dataset_dict['name'] = "coding-sample-2"
dataset_dict['title'] = "Coding Sample 2"
dataset_dict['notes'] = "Coding Sample from DPUE 1.1"
dataset_dict['url'] = "https://github.com/alexrashed/tu-dpue-lab1-ss18/blob/master/analyze.py"
mysite.call_action('package_create', dataset_dict)

mysite.action.resource_create(
    package_id='coding-sample-2',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='analyze.py',
    description = 'Analyzing Program used in DPUE Task 1.',
    upload=open('./RepositoryContents/analyze.py', 'rb'))
dataset_dict['name'] = "audio-sample-1"
dataset_dict['title'] = "Audio Sample 1"
dataset_dict['notes'] = "Audio Sample for DPUE 2"
dataset_dict['extras'] = [{"key": "Bitrate", "value": "19.7"}, {"key": "Length", "value": "6"}]
dataset_dict.pop('url')
mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='audio-sample-1',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='audio_2018-05-21_13-58-10.ogg',
    description = 'Audio File Recorded for DPUE Task 2.',
    upload=open('./RepositoryContents/audio_2018-05-21_13-58-10.ogg', 'rb'))
dataset_dict['name'] = "audio-sample-2"
dataset_dict['title'] = "Audio Sample 2"
dataset_dict['notes'] = "Audio Sample for DPUE 2"
dataset_dict['extras'] = [{"key": "Bitrate", "value": "20"}, {"key": "Length", "value": "5"}]
mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='audio-sample-2',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='audio_2018-05-21_13-58-24.ogg',
    description = 'Audio File Recorded for DPUE Task 2.',
    upload=open('./RepositoryContents/audio_2018-05-21_13-58-24.ogg', 'rb'))
dataset_dict['name'] = "video-sample-1"
dataset_dict['title'] = "Video Sample 1"
dataset_dict['notes'] = "Video Sample for DPUE 2"
dataset_dict['extras'] = [{"key": "Bitrate", "value": "541"}, {"key": "Length", "value": "10"}]
mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='video-sample-1',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='video_2017-07-04_21-19-20.mp4',
    description = 'Personal Video File used for DPUE Task 2.',
    upload=open('./RepositoryContents/video_2017-07-04_21-19-20.mp4', 'rb'))
dataset_dict['name'] = "video-sample-2"
dataset_dict['title'] = "Video Sample 2"
dataset_dict['notes'] = "Video Sample for DPUE 2"
dataset_dict['extras'] = [{"key": "Bitrate", "value": "1730"}, {"key": "Length", "value": "7"}]
mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='video-sample-2',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='video_2018-03-15_19-47-59.mp4',
    description = 'Personal Video File used for DPUE Task 2.',
    upload=open('./RepositoryContents/video_2018-03-15_19-47-59.mp4', 'rb'))

dataset_dict['name'] = "document-sample-1"
dataset_dict['title'] = "Document Sample 1"
dataset_dict['notes'] = "Document Sample for DPUE 1, containing the Exercise PDF of Task 2"
dataset_dict.pop('extras')
mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='document-sample-1',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='Exercise2.pdf',
    description = 'Exercise PDF of Task 2.',
    upload=open('./RepositoryContents/Exercise2.pdf', 'rb'))

dataset_dict['name'] = "document-sample-2"
dataset_dict['title'] = "Document Sample 2"
dataset_dict['notes'] = "Document Sample for DPUE 2"
dataset_dict['url'] = "https://github.com/alexrashed/tu-dpue-lab1-ss18/blob/master/docs/README.pdf"
mysite.call_action('package_create', dataset_dict)
mysite.action.resource_create(
    package_id='document-sample-2',
    url='dummy-value',  # ignored but required by CKAN<2.6
    name='README.pdf',
    description = 'Readme of Task 1 of DPUE.',
    upload=open('./RepositoryContents/README.pdf', 'rb'))











