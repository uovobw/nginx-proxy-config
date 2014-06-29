# Nginx Proxy Config

A small script to manage a battery of [nginx](http://nginx.org/) proxies using 
[Flask](http://flask.pocoo.org/) and (some) [bootstrap](http://getbootstrap.com/)

It supports multiple sites per proxy host with and without ssl.
*Very crude, should not be used in production.*

## Setup

Requirements:

    Flask
    paramiko

### Installation

install dependencies

    pip install -r requirements.txt

export the configuration location

    export AT_CONFIG=/path/to/settings.py

and then run with

    python app.py

### Configuration

the configuration is straightforward, the script requires the remote user to either be root
or to be able to write-access the files under /etc/nginx/ (or where nginx is installed)

The service is designed to be rarely updated, so there is no data persistence
layer other than a pickled file that gets re-serialized each time the configuration is
edited. Security was not a concern since the proxy host only runs nginx in an empty
debian installation.

## TODO

- improve code quality
- abstract and cleanup models
- input check and validation
- add database/storage
- clean up templates and javascript/css
- add multiple remotes to each frontend

## Author 
Andrea Lusuardi - uovobw@gmail.com
