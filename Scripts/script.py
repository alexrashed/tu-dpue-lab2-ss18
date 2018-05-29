#!/usr/bin/env python3
import configparser
import argparse
import sys
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument("command", help="Choose ldspace for the list of datasets in the dspace repository, lckan for the list of datasets in the ckan-repository and migrate to migrate data from ckan to dspace.")
parser.add_argument("-v", "--verbose", help="Outputs not only the name of the dataset, but the full information available", action="store_true")
args = parser.parse_args()

if args.command != "lckan" and args.command != "ldspace" and args.command != "migrate":
    print("Not a valid command, please check help.")
    sys.exit(1)

config = configparser.ConfigParser()
config.read('config.ini')
ckan_server_URL = config['CKAN']['ckan_server_URL']
ckan_api_key = config['CKAN']['ckan_api_key']
dspace_server_URL = config['DSPACE']['dspace_server_URL']


def list_ckan():
    if not ckan_server_URL:
        print("ckan_server_URL not configured in config.ini")
        sys.exit(1)

    ckan_response = requests.get(ckan_server_URL + "/api/3/action/package_list")
    if ckan_response.ok:
        json_data = ckan_response.json()
        if json_data["success"]:
            if not json_data["result"]:
                print("The Repository has no items.")
            else:
                for key in json_data["result"]:
                    if args.verbose:
                        verbose_response = requests.get(ckan_server_URL + "/api/3/action/package_show?id=" + key)
                        if verbose_response.ok:
                            verbose_json = verbose_response.json()
                            print(json.dumps(verbose_json["result"], indent=4, sort_keys=False))
                    else:
                        print(key)
    else:
        print("Could not connect to " + ckan_server_URL + "/api/3/action/package_list")


def list_dspace():
    if not dspace_server_URL:
        print("dspace_server_URL not configured in config.ini")
        sys.exit(1)

    headers = {'Accept': 'application/json'}
    dspace_response = requests.get(dspace_server_URL + "/rest/items", headers)
    if dspace_response.ok:
        json_data = dspace_response.json()
        if not json_data:
            print("The Repository has no items")
        else:
            for key in json_data:
                if args.verbose:
                    print(json.dumps(key, indent=4, sort_keys=False))
                else:
                    print(key['name'])

    else:
        print("Could not connect to " + dspace_server_URL + "/rest/items")


def migrate():
    if not ckan_server_URL:
        print("ckan_server_URL not configured in config.ini")
        sys.exit(1)
    if not ckan_api_key:
        print("ckan_api_key not configured in config.ini")
        sys.exit(1)
    print('TODO')

    # ckan_response = requests.get(ckan_server_URL + "/api/3/action/package_list", headers={'Authorization': ckan_api_key})
    # if ckan_response.ok:

    # Create the new schema in CKAN
    # Iterate over the organisations
        # Create the organisation
        # Iterate over the items
            # If item is in a group: Collection name is group
            # Else: Collection name is default (maybe orga name?)
            # if collection name does not exist, create
            # Create the Item in DSPACE
            # Download the file from CKAN, upload the file (bitstream) to DSPACE
                # https://stackoverflow.com/questions/33055773/adding-a-new-bitstream-to-dspace-item-using-dspace-rest-api
                # https://github.com/DSpace/DSpace/blob/master/dspace-rest/src/main/java/org/dspace/rest/BitstreamResource.java
            # Add the additional metadata to the DSPACE item
                # POST /items/{item id}/metadata - Add metadata to item. You must post an array of MetadataEntry.


if args.command == "lckan":
    list_ckan()
elif args.command == "ldspace":
    list_dspace()
elif args.command == "migrate":
    migrate()
