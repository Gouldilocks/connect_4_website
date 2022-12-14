# Here we set up the build for the NODE container
# We simply set the working directory within docker and also expose the port to our API, 8000
# Docker compose handles all the cross platform persistence via volumes so we don't need to worry about
#   copying over any of the actual code files for the backend.

# We are using python version 3.9
FROM python:3.9

# Set the working directory within docker image
WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

# expose port 8080
EXPOSE 8080