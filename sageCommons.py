import requests
import json
from requests.exceptions import HTTPError

class sageCommons:
    def __init__(self,endpoint,apiKey):
        self.endpoint = endpoint
        self.apiKey = apiKey
        self.packageCreateAction = '/api/3/action/package_create'
        self.resourceCreateAction = '/api/3/action/resource_create'
        self.authHeader = {'Authorization': self.apiKey}

    def uploadDataset(self,orgName,dataset):
        url = self.endpoint + self.packageCreateAction
        title = dataset['title']
        name = dataset['name']
        notes = dataset['notes']
        tags = [{'name': x } for x in dataset['tags']]

        payload = {'owner_org': orgName,
                    'title': title,
                    'name' : name,
                    'notes': notes,
                    'tags' : tags,
                }

        headers = self.authHeader
        try:
            response = requests.request("POST", url, headers=headers, json = payload)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

        responseJSON = response.json()
        result = responseJSON.get('result',None)
        datasetID = None

        if result is not None:
            datasetID = responseJSON['result']['id']
        
        return datasetID,response
    
    def uploadResource(self,datasetID,resource):
        url = self.endpoint + self.resourceCreateAction
        resourceName = resource['name']
        resourceDescription = resource['description']
        dataURL = resource['url']
        fileFormat = resource['format']

        payload = {'package_id': datasetID,
                    'name' : resourceName,
                    'description': resourceDescription,
                    'url': dataURL,
                    'format': fileFormat,
                }
        headers = self.authHeader
        try:
            response = requests.request("POST", url, headers=headers, json = payload)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

        return response

    def uploadDataForEntity(self,org,dataJSONFile):
        dataJSON = json.load(open(dataJSONFile))

        numDatasets = len(dataJSON)
        
        for i in range(numDatasets):
            iDataset = dataJSON[i]
            datasetID,response = self.uploadDataset(org,iDataset)
            if response.status_code != 200:
                print('Dataset upload not succesful.')
                print('Dataset: ' + str(iDataset['name']))
                print('Response code: ' + str(response.status_code))
                print('Response text: ' + str(response.text))
                break
            
            resources = dataJSON[i]['resource']
            numResources = len(resources)
            
            for j in range(numResources):
                iResource = resources[j]
                response = self.uploadResource(datasetID,iResource)
                if response.status_code != 200:
                    print('Dataset upload not succesful.')
                    print('Dataset: ' + str(iDataset['name']))
                    print('Resource: ' + str(iResource['name']))
                    print('Response code: ' + str(response.status_code))
                    print('Response text: ' + str(response.text))
                    continue