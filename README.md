# hello-flask
Hello world flask app

## Set Up pyb Repo
$ python -m venv venv
$ (venv) pip install pybuilder
$ pyb --start-project

## Run Flask app 
$ export FLASK_APP=app.py
$ python -m flask run

## Build docker image
$ docker build . -t hello-flask:0.0.1

## Run containerised app
$ docker run -d -p 5000:5000 hello-flask:0.0.2

## Call service
$ curl http://{host}:{port}/v1/models/hello-world:predict
