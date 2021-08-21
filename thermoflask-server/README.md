# About 

This is the Flask -section of the server project.

# Setup

## Dependencies

This project is designed to run with Python3 in a proper virtual environment. Requirements for Python packages after cloning the repository are inside the requirements.txt in this folder.

Following Debian packages will be required:

- libmariadb3 and libmariadb-dev, needed for MariaDB Python -connection
- LAMP stack packages. If you know what to do, you can use obviously any other reverse proxy


## Setup

## Flask-project
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

With SQL shell execute:

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

Then import schema.sql to create necessary tables. This can be done either by importing the file in command line or by copy & pasting the contents into SQL shell.

# Project configuration

Configure and create config.py based on config-sample.py. Generate your own API password to access the project with clients e.g. with openssl base64 -random utility and populate the mysql section with your own credentials.

# Running

Generally run-server-dev.sh and run-server-prod.sh files contain necessary command line statements to run the project. However production mode should be done e.g. behind gunicorn. The native HTTP server is inefficient to this task and meant for development.

# Behind gunicorn

To be added later

# SystemdD unit file creation

