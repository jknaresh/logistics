# Logistics

**Tech Stock**
* Python
* Django
* Mysql (for auth)
* arangodb (https://www.arangodb.com/download-major/ubuntu/)


Create DB:
create database logistics CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

**geojson polygon**
* http://geojson.io


**Fetch provider data**
* All
    **GET http://127.0.0.1:8000/provider/
* Fetch by email
    ** GET http://127.0.0.1:8000/provider/?email=ff.jonnala@gmail.com
    
https://www.arangodb.com/docs/stable/indexing-geo.html
https://www.arangodb.com/docs/3.4/appendix-deprecated-simple-queries-geo-queries.html#within
