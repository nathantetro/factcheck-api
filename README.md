# ⚙ Flemish Factcheck API

This project crawls Flemish factchecking sites (sites listed below), extracts all the relevant information and makes it available via a Python (Flask) RESTful API.

Sites crawled:
1. https://www.knack.be/nieuws/factcheck/
2. https://www.vrt.be/vrtnws/nl/rubrieken/desinformatie/check/

## Features Extracted
"FactCheckTitle" : Textual statement of the claim which is being verified
"FactCheckDescription" : Truth rating provided by the respective sites in its original form
"URL" : URL of the corresponding source page
"language" : Language of the factcheck. ("fr","nl")
"date" : : Date when the factcheck was published.
"publisher" : Publisher of the factcheck (organization).

## Usage
http://{host}/api/{publisher}
Example: http://127.0.0.1:5000/api/knack
