# Football injuries project

## Introduction

Welcome to the "Football Injuries Project"! This website is designed to provide users with access to information about injuries sustained by football players, as well as details about the teams and players associated with them.

In our project, you will be able to:

* Learn about various types of injuries that football players encounter.
* Access information about specific players and their teams.

We aim to create a user-friendly and informative resource for football enthusiasts, coaches, medical professionals, and anyone interested in the health and well-being of athletes. Our goal in future is to raise awareness about injuries in football and their consequences, as well as to provide valuable data for analysis and research.

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
POSTGRES_DB=<postgres_db>
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_HOST=<postgres_host>
POSTGRES_PORT=<postgres_port>
DEBUG=<True>

SMTP_USER=<smtp_user>
SMTP_PASSWORD=<smtp_password>
SMTP_HOST=<smtp_host>
SMTP_PORT=<smtp_port>
SMTP_SSL=<True>
```

* Install <a href="https://docs.docker.com/engine/install/" class="external-link" style="text-decoration: none" target="_blank"><strong>Docker</strong></a>

* Pull, build and run docker containers:

``` run commands
docker compose pull
docker compose build
docker compose up -d
```

* Follow link <a href="http://127.0.0.1" class="external-link" style="text-decoration: none" target="_blank"><strong>http://127.0.0.1:8000</strong></a>

* If all steps have been implemented, you will see something like this:
<image src="images/homepage.png" style="max-width: 100%; height: auto">

* or like this:
<image src="images/homepage_dark.png" style="max-width: 100%; height: auto">


## Deploy

* Rent virtual maschine with static IP / rent domain

* Create ssh

* Connect to server via ssh

* _Optionally (for rented domain) - add public ip to rented domain in domain settings_

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
* Pull and run docker containers:

```run
docker compose pull
docker compose up-d
```

* Check link <a href="#" class="external-link" style="text-decoration: none" target="_blank"><strong>https://your_domain</strong></a>

## Football Injuries Project - REST API Documentation

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

### Conclusion

This documentation provides a comprehensive overview of the REST API for the Football Injuries Project. You can use the provided endpoints to access data about teams, players, and injuries in a structured format.
