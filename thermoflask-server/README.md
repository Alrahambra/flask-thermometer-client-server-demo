# About 

This is the Flask -section of the server project.

# Setup

## Dependencies

This project is designed to run with Python3 in a proper virtual environment (venv). Requirements for Python packages after cloning the repository are inside the ```requirements.txt``` in this folder.

Following Debian packages will be required:

- libmariadb3 and libmariadb-dev, needed for MariaDB Python -connection. 
- LAMP stack packages. If you know what to do, you can use obviously anything else as a reverse proxy than Apache2.
- In some cases, the python3-wheel package has been required as well for MariaDB Python connection.

Debian 10 has been the only tested distribution with this project and seems to be working perfectly.

## Setup

## Flask-project initialization
After cloning this whole project, navigate to the thermoflask-server folder.

Create and activate venv:

```
python3 -m venv venv
. venv/bin/activate
```
Then install requirements with pip:
```
pip3 install -r requirements.txt
```


## Creating empty database and users, tables

With SQL shell execute following and remember to create a secure password for the user. It is required for the Flask-application to access the database in the ```config.py``` file you're going to create.:

``` sql
#Create database
CREATE DATABASE thermometerdata;

#Create user
CREATE USER 'thermometerdata'@'localhost' IDENTIFIED BY 'salasana_on_paras';

#Give permissions to user
GRANT ALL PRIVILEGES ON thermometerdata.* TO 'thermometerdata'@'localhost';

#Save changes
FLUSH PRIVILEGES;
```

Then import schema.sql to create necessary tables. This can be done either by importing the file in command line or by copy & pasting the contents into SQL shell by first selecting the correct database.

# Project configuration

Configure and create config.py based on config-sample.py. Generate your own API password to access the project with clients e.g. with openssl base64 -random utility and populate the MySQL section with your own credentials which you just created.

# Running (for development)

Generally run-server-dev.sh and run-server-prod.sh files contain necessary command line statements to run the project. However production mode should be done e.g. behind gunicorn. The native HTTP server is inefficient to this task and meant for development purposes only.

# Configuring apache2 with gunicorn

Gunicorn is a a well performing "Python WSGI HTTP Server for UNIX". Configuring this project with gunicorn instead of using the native and inefficient Flask HTTP server is ideal and it works well with the Apache2.

Gunicorn is already installed at this point as a requirement specified in the requirements.txt and available for the virtual environment. It can be tested on the server directory by issuing e.g.:

```gunicorn --bind 127.0.0.1:5000 wsgi:app```

Remember to ensure you're not attempting to bind into a port already in use.

# Systemd unit file creation

TODO:

Unix socket and Systemd service