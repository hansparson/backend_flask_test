# backend_flask_test

### SYSTEM RUN
    <br> `Python3.9`
    <br>`Ubuntu 20.04

### FIRST CONFIGURATION
    <br> run python -r requirements.txt

### How to Manage ORM DB 
    Database Runing on Postgree all seting i add on .env
1. make migrate file (alembic), for any change in your models
    <br>`export FLASK_APP=server.py'
    <br>`flask db migrate -d "models/migrations" -m "message"`
    <br> recheck your migrate file in `./models/migrations/versions`, cz cannot detect rename table/column automatically.
2. execute migration for your change in db
    <br>`flask db upgrade -d "models/migrations"`

### RUN SERVER
    <br> run server with `sh ./start-app.sh`
    <br> the server automatycly upgrade the database from "models/migrations"

### POSTMAN
    I also share postman File for testing with file name
    Backend_Test_TJ.postman_collection