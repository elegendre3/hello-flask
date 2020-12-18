# hello-flask
Hello world + gpt3 flask app

## Set Up pyb Repo
$ python -m venv venv
$ (venv) pip install pybuilder
$ pyb --start-project

## Run Flask app 
$ export FLASK_APP=app.py
$ python -m flask run
OR
$ python app.py

## Build docker image
$ docker build . -t hello-flask:0.0.1

# Build with secrets
$ DOCKER_BUILDKIT=1 docker build --secret id=mysecret,src=/path/to/secret_key.secret . -t hello-flask:0.0.3

## Run containerised app
$ docker run -d -p 5000:5000 hello-flask:0.0.2

## Call service
$ curl http://{host}:{port}/v1/models/hello-world:predict
