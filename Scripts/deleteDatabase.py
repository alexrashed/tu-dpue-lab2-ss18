#!/usr/bin/env python3
import configparser
from ckanapi import RemoteCKAN
import requests

config = configparser.ConfigParser()
config.read('config.ini')
ckan_server_URL = config['CKAN']['ckan_server_URL']
ckan_api_key = config['CKAN']['ckan_api_key']

mysite = RemoteCKAN(ckan_server_URL, apikey=ckan_api_key)

myResponse = requests.get(ckan_server_URL + "/api/3/action/package_list")
if(myResponse.ok):
    jData = myResponse.json()
    if jData["success"]:
        if jData["result"] == []:
            print("The Repository has no packages.")
        else:
            for key in jData["result"]:
                print(key)
                mysite.call_action('package_delete', {'id': key})
    else:
        print("Could not connect to " + ckan_server_URL + "/api/3/action/package_list")

myResponse = requests.get(ckan_server_URL + "/api/3/action/group_list")
if(myResponse.ok):
    jData = myResponse.json()
    if jData["success"]:
        if jData["result"] == []:
            print("The Repository has no groups.")
        else:
            for key in jData["result"]:
                print(key)
                mysite.call_action('group_delete', {'id': key})
    else:
        print("Could not connect to " + ckan_server_URL + "/api/3/action/group_list")
