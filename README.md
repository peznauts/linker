# Linker

Linker a service for URL simplification.

The hashing server responds to two methods, GET and HEAD.

More in-depth documentation can be seen [here](linker/static/linker.8).

----

## Create a simplified link

To create a simplified link run one of the following methods.

### GET

A get request will return a hashed URL of a given link.

``` shell
curl https://127.0.0.1:5000?link=https://peznauts.com/twitch
http://127.0.0.1:5000/9467ef6f0c613346dc9c812ed9b7568c0f20ff2b%
```

### HEAD

A HEAD request will return information about the hashed URL should it exist.

``` shell
$ curl --head http://127.0.0.1:5000/\?link\=https://peznauts.com/twitch
HTTP/1.0 200 OK
Content-Type: text/plain; charset="utf-8"
Content-Length: 62
X-Frame-Options: SAMEORIGIN
Cache-Control: public, max-age=120
Rendered-Link: http://127.0.0.1:5000/9467ef6f0c613346dc9c812ed9b7568c0f20ff2b
Server: Werkzeug/1.0.1 Python/3.8.7
Date: Sat, 20 Mar 2021 18:01:26 GMT
```

## Access a simplified link

### GET

``` shell
$ curl http://127.0.0.1:5000/9467ef6f0c613346dc9c812ed9b7568c0f20ff2b
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="https://peznauts.com/twitch">https://peznauts.com/twitch</a>.  If not click the link.%
```

### HEAD

Running a ``HEAD`` request against a simplified link will provide information
about the link.

``` shell
$ curl --head http://127.0.0.1:5000/9467ef6f0c613346dc9c812ed9b7568c0f20ff2b
HTTP/1.0 308 PERMANENT REDIRECT
Content-Type: text/html; charset=utf-8
Content-Length: 261
Location: https://peznauts.com/twitch
Referer: http://127.0.0.1:5000/9467ef6f0c613346dc9c812ed9b7568c0f20ff2b
Referrer-Policy: unsafe-url
Link-Used: 14
X-Frame-Options: SAMEORIGIN
Cache-Control: public, max-age=120
Server: Werkzeug/1.0.1 Python/3.8.7
Date: Sat, 20 Mar 2021 18:03:42 GMT
```

----

## Server setup

This application is a python installable and can be deployed in an almost
endless number of ways. For the purpose of example, the simple script
`server-setup.sh` can be used to deploy the application or derive ideas on the
application deployment.

## Test Server

A test server can be run by executing the ``runserver.py`` file within the ``assets``
folder within this repository.

``` shell
python3 ./runserver.py
```

The test server requires a database to run, by default the database used is
**sqllite**. While sqllite works, external database servers are recommended
for production workloads.

----

## Containerization

This repository publishes automatically publishes a container for easy
consumption. The container used with Linker is built on a UBI base images
and are made to run very lean.

### Building the linker container

Linker can run in a container and a UBI-minimal container file is included in
this repository.

#### Building

``` shell
$ podman build -f Containerfile -t linker
```

#### Pull Container

Container images for the latest Linker builds are automatically published on
various registries.

##### Github

``` shell
podman login https://docker.pkg.github.com -u $USERNAME
podman pull docker.pkg.github.com/peznauts/linker/linker:main
```

##### Quay.io

``` shell
$ podman pull quay.io/peznauts/linker
```

##### Docker Hub

``` shell
$ docker pull peznauts/linker
```

#### Running

Once you have the container on the system, running it is simple.

``` shell
$ podman run --network=host $CONTAINER_ID
```

When running in production it is highly recommended that Linker be setup with
an external database. This can be defined using an environment variable within
the container runtime.

``` shell
$ podman run --network=host -e LINKER_DB='mysql+pymysql://user:password@database-host/db-name' $CONTAINER_ID
```

> For deployment customization, please review the available environment variables; [Documentation](linker/static/linker.8)

Once running, the container will respond on port `5000`.
