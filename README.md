# Football injuries project

## Introduction

Welcome to the "Football Injury Project"! This website is designed to provide users with access to information about teams, players, and injuries sustained by players.

In our project, you will be able to:

* Learn about various types of injuries that football players encounter.
* Access information about specific players and their teams.

We aim to create a resource for anyone interested in the health and well-being of football players.

### You can use Football injuries at the following link

<p><a href="https://sportinj.ru/" class="external-link" style="text-decoration: none" target="_blank"><strong>sportinj.ru</strong></a></p>

## Install locally

* Clone repo:
```git clone https://github.com/alekseybeloded/football_injuries.git```

* Create file **_.env_** with variables:

```env
SECRET_KEY=<django_secret_key>
ALLOWED_HOSTS=<127.0.0.1>
INTERNAL_IPS=<127.0.0.1>
DEBUG=<True>

POSTGRES_DB=<postgres_db>
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_HOST=<postgres_host>
POSTGRES_PORT=<postgres_port>

SMTP_USER=<smtp_user>
SMTP_PASSWORD=<smtp_password>
SMTP_HOST=<smtp_host>
SMTP_PORT=<smtp_port>
SMTP_SSL=<True>

LOCATION=<cache_location>

CELERY_BROKER_URL=<celery_broker_url>

PROXY=<proxy_server>
```

* Install <a href="https://docs.docker.com/engine/install/" class="external-link" style="text-decoration: none" target="_blank"><strong>Docker</strong></a>

* Pull, build and run docker containers:

``` run commands
docker compose up -d --build
```

* Follow link <a href="http://127.0.0.1" class="external-link" style="text-decoration: none" target="_blank"><strong>http://127.0.0.1:8000</strong></a>

* If all steps have been implemented, you will see something like this:
<image src="images/homepage.png" style="max-width: 100%; height: auto">

* or like this:
<image src="images/homepage_dark.png" style="max-width: 100%; height: auto">


## Deploy

* Rent virtual machine with static IP / rent domain

* Create SSH

* Connect to server via SSH

* _Optionally (for rented domain) - add public IP to rented domain in domain settings_

* Install docker (follow <a href="https://docs.docker.com/engine/install/" class="external-link" style="text-decoration: none" target="_blank"><strong>instructions</strong></a> _include_ **_postinstall steps_**)

* Create **.env** file:
    * create variables from section **Install locally/Create file**
    * add public ip/host name and version for variables:

```env
ALLOWED_HOSTS=<www.your_domain,your_domain>
CSRF_TRUSTED_ORIGINS=<https://your_domain,https://www.your_domain>
VERSION=<v*.*.*>
DEBUG=False
```

* Create folders for nginx.conf:
``` run
mkdir nginx
mkdir nginx/ssl
mkdir nginx/conf.d
```

* Copy file **football_injuries/deploy/nginx/conf.d/nginx.conf** to folder _nginx/conf.d_
* Replace lines where are specified sportinj domain on your domain in **nginx.conf** file

* Create/copy recieved ssl certificates in folder **_nginx/ssl_** as:

        **your_domain.crt** your sertificate, intermediate certificate, root certificate

        **domain.key** private key

* Copy **docker-compose.yml** from **football_injuries/deploy/**:
* Pull, build and run docker containers:

```run
docker compose up -d --build
```

* Check link <a href="#" class="external-link" style="text-decoration: none" target="_blank"><strong>https://your_domain</strong></a>

## Football Injuries Project - REST API documentation

### Overview

The Football Injuries Project provides a REST API to access information about teams, players, and injuries. This API is built using Django REST Framework and allows for read-only access to the data.

### API Endpoints

The following endpoints are available in the REST API:

#### Teams

GET /teams/: Retrieve a list of all teams.

GET /teams/{id}/: Retrieve details of a specific team by ID.

#### Players

GET /players/: Retrieve a list of all players.

GET /players/{id}/: Retrieve details of a specific player by ID.

#### Injuries

GET /injuries/: Retrieve a list of all injuries.

GET /injuries/{id}/: Retrieve details of a specific injury by ID.

### Models

The API is built on the following models:

#### Team

name: The name of the team.

description: A brief description of the team.

#### Player

name: The name of the player.

description: A brief description of the player.

team: The team to which the player belongs.

#### Injury

name: The name of the injury.

description: A brief description of the injury.

player: The player who has the injury.

team: The team of the injured player.

## Testing the API

To test the API, you can use tools like Postman or cURL. Here are some example requests:

Get all teams

```bash
curl -X GET https://sportinj.ru/api/v1/teams/
```

Get a specific player

```bash
curl -X GET https://sportinj.ru/api/v1/players/70/
```

Get all injuries

```bash
curl -X GET https://sportinj.ru/api/v1/injuries/
```

## Conlusion

This documentation provides a comprehensive overview of the Football Injuries Project. You can use the website or the provided endpoints to access data about teams, players, and injuries. You can also install this project on your local machine or deploy it to a virtual machine with a static IP.
