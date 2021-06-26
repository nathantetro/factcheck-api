import json
from flask import Flask
from flask_cors import CORS
from util import util
from business import factCheckManager
from util.consoleColors import colors

app = Flask(__name__)
CORS(app)

print(
    colors.BOLD + colors.HEADER + "*-*-*-*-*-*-*-* WELCOME TO FACTCHECK HUB API *-*-*-*-*-*-*-*" + colors.ENDC)

factCheckManager.init_factchecks(initDatabase=True)


@app.route('/')
def index():
    return '<b>Factcheck API - Working</b><hr><br><br>Available endpoints:<br>' + json.dumps(util.get_endpoints(app))


@app.route('/api/all')
def all_factchecks():
    response = app.response_class(
        response=json.dumps(factCheckManager.get_all_factchecks(), indent=4, ensure_ascii=False, default=str).encode(
            'utf8'),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/vrt', methods=['GET'])
def vrt():
    response = app.response_class(
        response=json.dumps(factCheckManager.get_factcheck_from_publisher("VRT"), indent=4, ensure_ascii=False,
                            default=str).encode(
            'utf8'),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/knack', methods=['GET'])
def knack():
    response = app.response_class(
        response=json.dumps(factCheckManager.get_factcheck_from_publisher("KNACK"), indent=4, ensure_ascii=False,
                            default=str).encode('utf8'),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
