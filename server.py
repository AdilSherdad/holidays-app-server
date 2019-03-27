from flask import Flask, jsonify, json, escape, request
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
import  requests_cache

from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect()

app = Flask(__name__)

hol_url_template = 'https://calendarific.com/api/v2/holidays?country={c}&year={y}&api_key={k}'
BKEY='5953b75415d06e6fe300c2ee5d2be4d7771af5fc'
country1='PK'
year1='2019'
holidays=None
hol_url = hol_url_template.format(c=country1, y=year1,k = BKEY)

hs = [
{
  "date": {
    "datetime": {
      "day": 1,
      "month": 1,
      "year": 2019
    },
    "iso": "2019-01-01"
  },
  "description": "January 1 marks the beginning of the official New Year in Pakistan and is celebrated throughout the country as New Year\u2019s Day.",
  "locations": "All",
  "name": "New Year's Day",
  "states": "All",
  "type": [
    "National holiday"
  ]
}]



@app.route('/holiday', methods=['GET'])
def get_holiday():

	# resp = requests.get(hol_url).json()
	# holidays = resp['response']['holidays']
	# holiday=holidays[0]

	rows = session.execute("SELECT * FROM keyspaces.holidays")
	for row in rows:
		holiday = {'id':row.id, 'name': row.name, 'description': row.description, 'locations': row.locations, 'date': row.date }
		holidays.append(holiday)

	return jsonify(holidays), 200

	#respon.status_code = 200
	# or 400 or whatever

@app.route('/holiday/local', methods=['GET'])
def get_holiday_local():
	return jsonify(hs), 200

@app.route('/holiday', methods=['POST'])
def create_holiday():
	holidays=None

	hol_url = hol_url_template.format(c=country1, y=year1,k = BKEY)
	resp = requests.get(hol_url).json()
	holidays = resp['response']['holidays']
	holiday=holidays[0]

	print(holiday)

	for holi in holidays:
		if holi['name'] == request.form['name']:
			# holi['date']['iso']
			count_rows = session.execute("SELECT COUNT(*) FROM keyspaces.history")

			for c in count_rows:
				last_id = c.count
			last_id += 1

			rows = session.execute("INSERT INTO keyspaces.history(id, name, description, locations, date) VALUES(%s, %s, %s, %s, %s)", (last_id, request.form['name'], request.form['description'], holi['locations'], holi['date'].iso))

			return jsonify({'message':'holiday created successfully'}), 201

	return jsonify({'error': 'holiday not created'}), 400

@app.route('/holiday/<int:id>', methods=['PUT'])
def update_holiday(id):

	if not request.form or not 'name' in request.form:
		return jsonify({'Error': 'holiday not found'}), 404

	rows = session.execute("""UPDATE keyspaces.history SET name=%(name)s description=%(description)s WHERE id=%(id)s""", {'id': id, 'name': request.form['name'], 'description': request.form['description']})

	print('after update')

	return jsonify({'message':'updated: /holiday{}'.format(id)}), 200

@app.route('/holiday/<int:id>', methods=['DELETE'])
def delete_holiday(id):

	if not id:
		return jsonify({'Error': 'The id is needed to delete'}), 400

	resp = session.execute("""DELETE FROM keyspaces.history WHERE id={}""".format(id))

	return jsonify({'message': 'deleted: /holiday/{}'.format(id)}), 200



if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080,debug=True)
