import json
from flask import Flask
from flask_cors import CORS
from util import util
from business import factCheckManager
from util.consoleColors import colors
from util.util import convert_factchecks_to_json

app = Flask(__name__)
CORS(app)

print(
    colors.BOLD + colors.HEADER + "*-*-*-*-*-*-*-* WELCOME TO FACTCHECK HUB API *-*-*-*-*-*-*-*" + colors.ENDC)

factChecksInitialised = False
while factChecksInitialised is False:
    factCheckManager.init_factchecks(initDatabase=True)
    factChecksInitialised = True


@app.route('/')
def index():
    return '<b>Factcheck API - Working</b><hr><br><br>Available endpoints:<br>' + json.dumps(util.get_endpoints(app))


@app.route('/api/all', methods=['GET'])
def all_factchecks():
    response = app.response_class(
        response=convert_factchecks_to_json(factCheckManager.get_all_factchecks()),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/vrt', methods=['GET'])
def vrt():
    jsonVrt = convert_factchecks_to_json(factCheckManager.get_factcheck_from_publisher("VRT"))
    response = app.response_class(
        response=jsonVrt,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/knack', methods=['GET'])
def knack():
    response = app.response_class(
        response=convert_factchecks_to_json(factCheckManager.get_factcheck_from_publisher("KNACK")),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
