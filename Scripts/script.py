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
    sys.exit(0)
config = configparser.ConfigParser()
config.read('config.ini')
ckan_server_URL = config['CKAN']['ckan_server_URL']
dspace_server_URL = config['DSPACE']['dspace_server_URL']
if args.command == "lckan":
    myResponse = requests.get(ckan_server_URL + "/api/3/action/package_list")
    if(myResponse.ok):
        jData = myResponse.json()
        if jData["success"]:
            if jData["result"] == []:
                print("The Repository has no items.")
            else:
                if args.verbose:
                    for key in jData["result"]:
                        verboseResponse = requests.get(ckan_server_URL + "/api/3/action/package_show?id=" + key)
                        if(verboseResponse.ok):
                            verboseJson = verboseResponse.json()
                            print(json.dumps(verboseJson["result"], indent=4, sort_keys=False))
                else:
                    for key in jData["result"]:
                        print(key)
    else: 
        print("Could not connect to " + ckan_server_URL + "/api/3/action/package_list")
if args.command == "ldspace":
    headers = {'Accept': 'application/json'}
    myResponse = requests.get(dspace_server_URL + "/rest/items", headers)
    if(myResponse.ok):
        jData = myResponse.json()
        print(jData)
        if jData == []:
            print("The Repository has no items")
        else:
            if args.verbose:
                for key in jData:
                    print(json.dumps(key, indent=4, sort_keys=False))
            else:
                for key in jData:
                    print(key['name'])
    else:
        print("Could not connect to " + dspace_server_URL + "/rest/items")
if args.command == "migrate":
    #TODO
    print()








