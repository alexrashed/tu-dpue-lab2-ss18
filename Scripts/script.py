#!/usr/bin/env python3
import configparser
import argparse
import sys
import requests
import json
import uuid
import urllib.request

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
dspace_email = config['DSPACE']['dspace_email']
dspace_password = config['DSPACE']['dspace_password']

# IDs for created communities
community_ids = {}

# Unique names for the default collection per community (if no group is defined for an item)
default_collection_ids = {}

# IDs for created non-default collections per community
collection_ids = {}


def list_ckan():
    """
    Lists all packages in the CKAN repository.
    """
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
    """
    Lists all items in the DSpace repository.
    """
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
    """
    Migrates the content of the CKAN repository to the DSpace repository.
    """
    if not ckan_server_URL:
        print("ckan_server_URL not configured in config.ini")
        sys.exit(1)
    if not ckan_api_key:
        print("ckan_api_key not configured in config.ini")
        sys.exit(1)
    if not dspace_email:
        print("dspace_email not configured in config.ini")
        sys.exit(1)
    if not dspace_password:
        print("dspace_password not configured in config.ini")
        sys.exit(1)

    # Login to DSpace
    dspace_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'email': dspace_email, 'password': dspace_password}
    dspace_session = requests.Session()
    dspace_response = dspace_session.post(dspace_server_URL + "/rest/login", headers=dspace_headers, data=data)
    if not dspace_response.ok:
        print("DSpace login failed: " + str(dspace_response.status_code))
        sys.exit(1)

    # Create the multimedia schema in DSpace
    create_schema(dspace_session)

    # Create the communities in DSpace
    create_communities(dspace_session)

    # Create the items
    create_items(dspace_session)


def create_schema(session):
    """
    Creates a new schema in DSpace for multimedia (bitrate + length metadata fields).

    :param session: current requests session (has to be logged in to DSpace)
    """
    # TODO switch to multimedia and test
    schema_prefix = "multimedia1"
    schema_get_response = session.get(dspace_server_URL + "/rest/registries/schema/" + schema_prefix)
    if schema_get_response.ok:
        print("Schema already exists.")
        return

    schema_creation_payload = {'namespace': 'http://tuwien.ac.at/dpue/' + schema_prefix, "prefix": schema_prefix}
    schema_creation_headers = {'Content-Type': 'application/json'}
    schema_creation_response = session.post(dspace_server_URL + "/rest/registries/schema/",
                                            headers=schema_creation_headers,
                                            json=schema_creation_payload)
    if not schema_creation_response.ok:
        print("DSpace schema creation failed: " + str(schema_creation_response.status_code))
        sys.exit(1)

    schema_add_bitrate_headers = {"Accept": "'/'", 'Content-Type': 'application/json'}
    schema_add_bitrate_payload = {'element': 'Bitrate', "qualifier": "Bitrate",
                                  "description": "Bitrate of Audio- or Videofile"}
    schema_add_bitrate_response = session.post(
        dspace_server_URL + "/rest/registries/schema/" + schema_prefix + "/metadata-fields",
        headers=schema_add_bitrate_headers, json=schema_add_bitrate_payload)
    if not schema_add_bitrate_response.ok:
        print("DSpace bitrate metadata field creation failed: " + str(schema_add_bitrate_response.status_code))
        sys.exit(1)

    schema_add_length_headers = {"Accept": "'/'", 'Content-Type': 'application/json'}
    schema_add_length_payload = {'element': 'Length', "qualifier": "Length",
                                 "description": "Length of Audio- or Videofile"}
    schema_add_length_response = session.post(
        dspace_server_URL + "/rest/registries/schema/" + schema_prefix + "/metadata-fields",
        headers=schema_add_length_headers, json=schema_add_length_payload)
    if not schema_add_length_response.ok:
        print("DSpace length metadata field creation failed: " + str(schema_add_length_response.status_code))
        sys.exit(1)


def create_communities(dspace_session):
    # Get the organisations in CKAN
    ckan_response = requests.get(ckan_server_URL + "/api/3/action/organization_list",
                                 headers={'Authorization': ckan_api_key})
    if not ckan_response.ok:
        print("Reading ckan organizations failed.")
        sys.exit(1)
    organization_keys = ckan_response.json()["result"]
    if not organization_keys:
        print("No organisations in CKAN.")
    else:
        # Iterate over the organisations
        for key in organization_keys:
            # Create the community
            print("Creating DSpace community for CKAN organization: " + key)
            organization_response = requests.get(ckan_server_URL + "/api/3/action/organization_show?id="
                                                 + key)
            if not organization_response.ok:
                print("CKAN organization details could not be read: " + str(organization_response.status_code))
                sys.exit(1)

            organization = organization_response.json()["result"]
            data = json.dumps({
                'name': organization["display_name"],
                'sidebarText': organization["name"],
                'shortDescription': organization["description"]
            })
            dspace_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            dspace_response = dspace_session.post(dspace_server_URL + "/rest/communities", headers=dspace_headers,
                                                  data=data)
            if not dspace_response.ok:
                print("DSpace community could not be created: " + str(dspace_response.status_code))
                sys.exit(1)
            community_ids[key] = dspace_response.json()["uuid"]
            print("Created DSpace community with UUID " + community_ids[key])


def create_items(dspace_session):
    # Get the packages from CKAN
    packages_response = requests.get(ckan_server_URL + "/api/3/action/package_list")
    if not packages_response.ok:
        print("CKAN packages could not be read: " + str(packages_response.status_code))
        sys.exit(1)
    package_keys = packages_response.json()["result"]

    # Iterate over the packages
    for package_key in package_keys:
        package_response = requests.get(ckan_server_URL + "/api/3/action/package_show?id=" + package_key)
        if not package_response.ok:
            print("CKAN package info could not be read: " + str(package_response.status_code))
            sys.exit(1)
        package = package_response.json()["result"]

        community = community_ids[package["organization"]["name"]]
        collection_id = get_or_create_collection_id(dspace_session, community, package["groups"])

        data = json.dumps({
            'name': package["name"]
        })
        print("Creating DSpace item " + data + " in collection with ID " + collection_id)
        dspace_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        dspace_response = dspace_session.post(dspace_server_URL + "/rest/collections/" + collection_id + "/items",
                                              headers=dspace_headers, data=data)
        if not dspace_response.ok:
            print("DSpace item could not be created: " + str(dspace_response.status_code))
            sys.exit(1)

        item_id = dspace_response.json()["uuid"]
        print("Created DSpace item with ID " + item_id)

        if not package["resources"]:
            print("Package does not contain any resources, continue.")
            continue

        # Add the bitstreams
        for resource in package["resources"]:
            create_bitstreams(dspace_session, item_id, resource)

        # TODO: Add all additional data of the item (besides the name)

        # TODO: Add extras (additional metadata for multimedia)
        # If there is a custom schema:
            # Add the additional metadata to the DSPACE item
                # POST /items/{item id}/metadata - Add metadata to item. You must post an array of MetadataEntry.

        # TODO: Invoke refreshing the index / solr


def get_or_create_collection_id(dspace_session, community, groups):
    """
    Finds / creates the collection in the given community and group.

    :param dspace_session: logged in DSpace session
    :param community: ID of the community to create the collection in. if not defined, a default community will be created / used
    :param groups: list of groups of the item. If empty, a default collection will be created / used. Otherwise the first group entry will be used as collection name
    :return: UUID of the collection to use
    """
    if not groups:
        # If a default collection for the community has already been created, just return it:
        try:
            return default_collection_ids[community]
        except KeyError:
            # Create a UUID to make sure there is no conflicting collection existing
            collection = {"name": str(uuid.uuid4())}
    else:
        # The group name is unique, if we already created one for the group name, just return the ID
        try:
            return collection_ids[community][groups[0]["name"]]
        except KeyError:
            collection = {"name": groups[0]["display_name"], "shortDescription": groups[0]["description"]}

    print("Creating DSpace collection for community with ID " + community + ": " + str(collection))
    dspace_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    dspace_response = dspace_session.post(dspace_server_URL + "/rest/communities/" + community + "/collections",
                                          headers=dspace_headers, data=json.dumps(collection))
    if not dspace_response.ok:
        print("DSpace collection could not be created: " + str(dspace_response.status_code))
        sys.exit(1)

    new_id = dspace_response.json()["uuid"]
    print("Created DSpace collection with UUID " + new_id)

    # Store the new id to prevent duplicated collections
    if not groups:
        default_collection_ids[community] = new_id
    else:
        try:
            collection_ids[community][groups[0]["name"]] = new_id
        except KeyError:
            collection_ids[community] = {groups[0]["name"] : new_id}
    return new_id


def create_bitstreams(dspace_session, item_id, resource):
    data = json.dumps({
        'name': resource["name"],
        'format': resource["format"],
        'mimetype': resource["mimetype"],
        'description': resource["description"]
    })
    print("Creating DSpace bitstream " + data + " for item with ID " + item_id)
    dspace_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    dspace_response = dspace_session.post(dspace_server_URL + "/rest/items/" + item_id + "/bitstreams?name=" + resource["name"],
                                          headers=dspace_headers, data=data)
    if not dspace_response.ok:
        print("DSpace bitstream could not be created: " + str(dspace_response.status_code))
        sys.exit(1)

    bitstream_id = dspace_response.json()["uuid"]
    print("Created DSpace bitstream with ID " + bitstream_id)

    dspace_headers = {'Content-Type': 'application/octet-stream', 'Accept': 'application/json'}
    data = urllib.request.urlopen(resource["url"]).read()
    dspace_response = dspace_session.put(dspace_server_URL + "/rest/bitstreams/" + bitstream_id + "/data",
                                          headers=dspace_headers, data=data)
    if not dspace_response.ok:
        print("DSpace bitstream data could not be written: " + str(dspace_response.status_code))
        sys.exit(1)
    print("Created DSpace bitstream data for bitstream with ID " + bitstream_id)

    # POST /items/{item id}/bitstreams - Add bitstream to item. You must post a Bitstream.
    # PUT /bitstreams/{bitstream id}/data - Update data/file of bitstream. You must put the data


    # TODO: Add bitstream
    # Download the file from CKAN, upload the file (bitstream) to DSPACE
    # https://stackoverflow.com/questions/33055773/adding-a-new-bitstream-to-dspace-item-using-dspace-rest-api
    # https://github.com/DSpace/DSpace/blob/master/dspace-rest/src/main/java/org/dspace/rest/BitstreamResource.java
    # PUT /bitstreams/{bitstream id}/data - Update data/file of bitstream. You must put the data



if args.command == "lckan":
    list_ckan()
elif args.command == "ldspace":
    list_dspace()
elif args.command == "migrate":
    migrate()