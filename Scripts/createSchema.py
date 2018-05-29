import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')
ckan_server_URL = config['CKAN']['ckan_server_URL']
dspace_server_URL = config['DSPACE']['dspace_server_URL']
dspace_email = config['DSPACE']['dspace_email']
dspace_password = config['DSPACE']['dspace_password']
payloadHeaders = {"Accept": "'/'", 'Content-Type': 'application/x-www-form-urlencoded'}
payloadLogin = {'email': dspace_email, 'password': dspace_password}
s = requests.Session()
loginRespone = s.post(dspace_server_URL + "/rest/login", headers=payloadHeaders, data=payloadLogin)
cookie = loginRespone.headers["Set-Cookie"]
schemaPrefix = "dpue"
schemaCreationPayload = {'namespace': 'Audiovisuell', "prefix": schemaPrefix}
schemaCreationHeaders = {"Accept": "'/'", 'Content-Type': 'application/json'}

schemaCreationResponse = s.post(dspace_server_URL +  "/rest/registries/schema/", headers=schemaCreationHeaders, json=schemaCreationPayload)
schemaAddBitrateHeaders =  {"Accept": "'/'", 'Content-Type': 'application/json'}
schemaAddBitratePayload =  {'element': 'Bitrate', "qualifier": "Bitrate", "description": "Bitrate of Audio- or Videofile"}
schemaAddBitrateResponse = s.post(dspace_server_URL +  "/rest/registries/schema/" + schemaPrefix + "/metadata-fields", headers=schemaAddBitrateHeaders, json=schemaAddBitratePayload)

schemaAddLengthHeaders =  {"Accept": "'/'", 'Content-Type': 'application/json'}
schemaAddLengthPayload =  {'element': 'Length', "qualifier": "Length", "description": "Length of Audio- or Videofile"}
schemaAddLengthResponse = s.post(dspace_server_URL +  "/rest/registries/schema/" + schemaPrefix + "/metadata-fields", headers=schemaAddLengthHeaders, json=schemaAddLengthPayload)
