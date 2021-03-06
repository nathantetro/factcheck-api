# ⚙ Flemish Factcheck API

This project crawls Flemish factchecking sites (sites listed below), extracts all the relevant information in a Postgresql database and makes it available via a Python (Flask) RESTful API in JSON format.

Sites crawled:
1. https://www.knack.be/nieuws/factcheck/
2. https://www.vrt.be/vrtnws/nl/rubrieken/desinformatie/check/

## Features Extracted
"title" : Title of the factcheck. <br>
"description" : Short description of the factcheck.<br>
"URL" : URL of the article. <br>
"language" : Language of the factcheck. ("fr","nl") <br>
"date" :  Date when the factcheck was published. <br>
"publisher" : Publisher of the factcheck (organization). <br>
"thumbnail" : Thumbnail of the article. <br>


## Usage
Run app.py. Wait until everything has been initilialized.<br> Then go to the app's url. For example: http://127.0.0.1:5000/api/knack

## 
<a href="https://factcheck-scraper-api.herokuapp.com/">Deployed with Heroku. 
<img src="https://cdn.iconscout.com/icon/free/png-256/heroku-225989.png" alt="HEROKU LOGO" width="25px" height="25px"></a>

