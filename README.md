# ⚙ Flemish Factcheck API

This project crawls Flemish factchecking sites (sites listed below), extracts all the relevant information in a Postgresql database and makes it available via a Python (Flask) RESTful API in JSON format.

Sites crawled:
1. https://www.knack.be/nieuws/factcheck/
2. https://www.vrt.be/vrtnws/nl/rubrieken/desinformatie/check/

## Features Extracted
"title" : Textual statement of the claim which is being verified <br>
"description" : Truth rating provided by the respective sites in its original form <br>
"URL" : URL of the corresponding source page <br>
"language" : Language of the factcheck. ("fr","nl") <br>
"date" :  Date when the factcheck was published. <br>
"publisher" : Publisher of the factcheck (organization). <br>

## Usage
Example: http://127.0.0.1:5000/api/knack 
