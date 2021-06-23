# ⚙ Flemish Factcheck API

This project crawls Flemish factchecking sites (sites listed below), extracts all the relevant information and makes it available via a Python (Flask) RESTful API.

Sites crawled:
1. https://www.knack.be/nieuws/factcheck/
2. https://www.vrt.be/vrtnws/nl/rubrieken/desinformatie/check/

## Features Extracted
"FactCheckTitle" : Textual statement of the claim which is being verified <br>
"FactCheckDescription" : Truth rating provided by the respective sites in its original form <br>
"URL" : URL of the corresponding source page <br>
"language" : Language of the factcheck. ("fr","nl") <br>
"date" : : Date when the factcheck was published. <br>
"publisher" : Publisher of the factcheck (organization). <br>

## Usage
http://{host}/api/{publisher} <br>
Example: http://127.0.0.1:5000/api/knack <br>
