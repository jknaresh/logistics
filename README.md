# Logistics

**Tech Stock**
* Python
* Django
* Mysql (for auth)
* arangodb (https://www.arangodb.com/download-major/ubuntu/)

****
**Why Arangodb**

About performance
https://www.arangodb.com/performance/

`Full GeoJSON support with all geo primitives, including multi-polygons or multi-line strings; increased query and 
filtering functionalities, and performance optimized.`

https://www.arangodb.com/arangodb-3-4/
****


**API Documentation**

* Create Provider API
~~~~
Method: POST

URL: http://127.0.0.1:8000/provider/

POST DATA:

name = "name"
email = "email"
mobile = "mobile no"
language = "language"
currency = "currency"

JSON Response:

{"status": true}
~~~~

* Read Provider(s)
~~~~
Method: GET

URL: http://127.0.0.1:8000/provider/

GET DATA:

email = "email" (optional field)

JSON Response:

[{"name": "name", "email": "email", "ph_no": "ph_no", "language": "language", "currency": "$"} ...]

~~~~
* Update Provider
~~~~
Method: POST

URL: http://127.0.0.1:8000/provider/

POST DATA:

email = "email"

Optional Data:

name = "name"
mobile = "mobile no"
language = "language"
currency = "currency"

JSON Response:

{"status": true}

~~~~
* Delete Provider
~~~~
Method: POST

URL: http://127.0.0.1:8000/provider/

POST DATA:

email = "email"
action = "delete"

JSON Response:

{"status": true}

~~~~

**Service area API**
* Create Service area API
~~~~
Method: POST

URL: http://127.0.0.1:8000/service-area/

POST DATA:

email = "email"
geojson = "polygon json data"
polygon_name = "polygon_name"
price = "price"

JSON Response:

{"status": true}
~~~~

* Read service area
~~~~
Method: GET

URL: http://127.0.0.1:8000/service-area/

GET DATA:

email = "email" (optional field)

JSON Response:

[{"geojson": {"type": "Polygon", "coordinates": [[[78.46420526504517, 17.40498767390072], [78.46248865127563, 17
.406646158987854], [78.46085786819458, 17.411641998415337], [78.45718860626219, 17.41731333908239], [78.45242500305176, 17.426772006420553], [78.44869136810303, 17.425748364771177], [78.44791889190674, 17.419442605633275], [78.4513521194458, 17.40687138419703], [78.45289707183838, 17.403554403061104], [78.4548282623291, 17.40437341634564], [78.46109390258789, 17.402981091578468], [78.46414089202881, 17.403922959493272], [78.46420526504517, 17.40498767390072]]]}, "polygon_name": "test 1", "price": "56"}]
~~~~

* Update service area
~~~~
Method: POST

URL: http://127.0.0.1:8000/service-area/

POST DATA:

email = "email"

Optional Data:

geojson = "polygon json data"
polygon_name = "polygon_name"
price = "price"

JSON Response:

{"status": true}
~~~~

* Delete Service Area
~~~~
Method: POST

URL: http://127.0.0.1:8000/service-area/

POST DATA:

email = "email"
action = "delete"

JSON Response:

{"status": true}
~~~~

**Find Polygon API**
~~~~
Method: GET

URL: http://127.0.0.1:8000/service-provider/

GET DATA:

lat=78.4529560804367
lng=17.4173210167708

JSON Response:

[{"name": "jonnala", "polygon_name": "test 1", "price": "56", "geojson": {"type": "Polygon", "coordinates": [[[78
.46420526504517, 17.40498767390072], [78.46248865127563, 17.406646158987854], [78.46085786819458, 17.411641998415337], [78.45718860626219, 17.41731333908239], [78.45242500305176, 17.426772006420553], [78.44869136810303, 17.425748364771177], [78.44791889190674, 17.419442605633275], [78.4513521194458, 17.40687138419703], [78.45289707183838, 17.403554403061104], [78.4548282623291, 17.40437341634564], [78.46109390258789, 17.402981091578468], [78.46414089202881, 17.403922959493272], [78.46420526504517, 17.40498767390072]]]}}]
~~~~


****
Create DB:
create database logistics CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

**geojson polygon**
* http://geojson.io




**Fetch provider data**
* Get All Provider Documents

    GET http://127.0.0.1:8000/provider/
    
* Fetch by email

    GET http://127.0.0.1:8000/provider/?email=ff.jonnala@gmail.com

https://www.arangodb.com/docs/stable/indexing-geo.html

https://www.arangodb.com/docs/3.4/appendix-deprecated-simple-queries-geo-queries.html#within
