# This docker file is used for local development via docker-compose
# Creating image based on official python3 image
FROM python:3.10

# Fix python printing
ENV PYTHONUNBUFFERED=1

# Installing all python dependencies
COPY requirements/ requirements/

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    apt-get install libpq-dev

# Upgrade pip
RUN pip install --upgrade pip

RUN pip install -r requirements/production.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/

EXPOSE 8000

CMD [ "./scripts/start.sh" ]
