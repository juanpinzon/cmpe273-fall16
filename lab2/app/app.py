import logging
from flask import json
from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne import Application, srpc, ServiceBase, Decimal, Unicode
from spyne.server.wsgi import WsgiApplication
import requests
from model import *



class CheckCrimeService(ServiceBase):
    @srpc(Decimal, Decimal, Decimal, _returns=Unicode)
    def checkcrime(lat, lon, radius):
        # Get the information from the CrimeReport API
        url = 'https://api.spotcrime.com/crimes.json'        
        params = {'lat':lat, 'lon':lon, 'radius':radius, 'key':'.'}
        input_data = requests.get(url=url, params=params)        
        input_json = json.loads(input_data.text)               #Convert response to JSON
        output_data = CrimeReport(input_json)                  #CrimeReport processes the input data

        #Create the output_json
        output_json = {
            "total_crime" : output_data.total_crime,
            "the_most_dangerous_streets" : output_data.the_most_dangerous_streets,
            "crime_type_count" : output_data.crime_type_count,
            "event_time_count" : output_data.event_time_count
        }

        return output_json


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    #Keep track of events using a log system
    logging.basicConfig(level=logging.DEBUG)

    # Creates the application using HttpRpc as input protocol and JsonDocument as output protocol
    application = Application([CheckCrimeService], 'checkcrime',
        in_protocol=HttpRpc(validator='soft'), out_protocol=JsonDocument(ignore_wrappers=True))

    #Use wsgi instead of flask
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()