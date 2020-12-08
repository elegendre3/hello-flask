# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.6-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY logging_conf.py app.py requirements.txt ./

# Install production dependencies.
RUN pip install --no-cache-dir -r ./requirements.txt


# Run flask app alone (no gunicorn)
# ENTRYPOINT ["python"]
# CMD ["app.py"]


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :5000 --workers 1 --threads 8 app:app
