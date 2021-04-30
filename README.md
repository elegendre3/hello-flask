# hello-flask
Hello world flask app with docker packaging

## Set Up Env
### venv
`$ python -m venv venv`

### pyenv
`$ pyenv virtualenv 3.6.8 flask_env`
`$ pyenv local flask_env`

###Set Up pyb Repo
`$ (venv) pip install pybuilder`
`$ pyb --start-project`

## Run Flask app 
`$ export FLASK_APP=src/main/python/run.py`
`$ python -m flask run`
OR
`$ cd src/main/python`
`$ python -m run`

## Build docker image
`$ docker build . -t hello-flask:0.0.<v>`

# Build with secrets
`$ DOCKER_BUILDKIT=1 docker build --secret id=mysecret,src=/path/to/secret_key.secret . -t hello-flask:0.0.3`

## Run containerised app
`$ docker run -d -p 0.0.0.:5000:5000 hello-flask:0.0.<v>`

## Call service
`$ curl http://{host}:{port}/hello-world:predict`
