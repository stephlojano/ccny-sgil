import requests
import json 
import urllib
import warnings
import os 
from ._exceptions import *

warnings.formatwarning = warning_format

class here_API:
    def __init__(self, apiKey=None, credentials_file=None):
        if (apiKey is None) and (credentials_file is None):
            raise CredentialsMissing()
        elif not (apiKey is None or credentials_file is None):
            warnings.warn(f"Two credentials options found. Extracting credentials from apiKey")
        elif credentials_file is not None: 
            if not os.path.isfile(credentials_file):
                raise CredentialsFileError()
        
        self._credentials = {}
        if apiKey: 
            self._credentials['apiKey'] = apiKey
        else:
            with open(credentials_file, 'r') as credentials_json:
                self._credentials = json.load(credentials_json)['apiKey']
        
        self.check_credentials()

        self.free_flow_model = None
        self.result = None
    
    def set_energy_model(self, speeds=None, energy_consumption=None, model=None):
        if (speeds is None or energy_consumption is None) and model is None:
            EnergyModelError(speeds, energy_consumption, model)
        
        if model: 
            self.free_flow_model = model 
        else:
            self.free_flow_model = []
            for idx, speed in enumerate(speeds):
                self.free_flow_model.append(speed)
                self.free_flow_model.append(energy_consumption[idx])
            
        return self.free_flow_model

    def make_request(self, origin, destination, time=None):
        api_tag = self._build_credentials_tags()
        self.origin = f'&origin={origin[0]},{origin[1]}'
        self.dest = f'&destination={destination[0]},{destination[1]}'

        if time: time = '&departureTime=' + time
        else: time = ''

        if self.free_flow_model: ev_field = self._transform_energy_model()  
        else: ev_field = ''

        # build and make the the request 
        api_request = f'https://router.hereapi.com/v8/routes?transportMode=car{self.origin}{self.dest}{time}{ev_field}&return=summary,polyline,travelSummary,actions{api_tag}'
        response = requests.get(api_request)

        self.result = response.json()

        if not self.result:
            raise ResponseError

        return self.result
    
    def get_energy_consumption(self):
        if self.result: 
            return self.result['routes'][0]['sections'][0]['summary']['consumption']
        else:
            raise ResponseError()
    
    def get_route_distance(self):
        if self.result:
            return self.result['routes'][0]['sections'][0]['summary']['length']
        else:
            raise ResponseError()
    
    def get_route_duration(self):
        if self.result:
            return self.result['routes'][0]['sections'][0]['summary']['duration']
        else:
            raise ResponseError()
    
    def check_credentials(self):
        api_tag = self._build_credentials_tags()
        testorg = (40.667864, -73.994026)
        testdest = (40.678123, -73.990967)

        api_origin = f'&origin={testorg[0]},{testorg[1]}'
        api_dest = f'&destination={testdest[0]},{testdest[1]}'

        here_api_request = f'https://router.hereapi.com/v8/routes?transportMode=car{api_origin}{api_dest}&return=summary,polyline{api_tag}'
        response = requests.get(here_api_request).json()
        if 'error' in response.keys():
            raise CredentialsError()
        else:
            print('Credentials OK')

    def _transform_energy_model(self):
        api_ev_field = '&ev[freeFlowSpeedTable]='

        for element in self.free_flow_model:
            api_ev_field += f'{element},'
        
        return api_ev_field[:-1]
    
    def _build_credentials_tags(self):
        return f'&apiKey={self._credentials["apiKey"]}'
