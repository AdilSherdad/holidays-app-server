from flask import Flask, jsonify, json
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
import  requests_cache


app = Flask(__name__)

key = '31d1aba5-0d2c-462f-90ff-fb20ce66918e'

def __init__(self, key):
        self.key = key
@app.route('/Hol', methods=['GET'])
def holidays():
        url = 'https://holidayapi.com/v1/holidays?'

        if parameters.has_key('key') is False:
            parameters['key'] = self.key

        response = requests.get(url, params=parameters);
        data = json.loads(response.text)

        if response.status_code != 200:
            if data.has_key('error') is False:
                data['error'] = 'Unknown error.'

        return data

if __name__ == '__main__':
	app.run(debug=True)