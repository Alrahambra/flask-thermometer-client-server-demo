# About 

This is the Flask -section of the server project.

# Setup

## Dependencies

This project is designed to run with Python3 in a proper virtual environment (venv). Requirements for Python packages after cloning the repository are inside the ```requirements.txt``` in this folder.

Following Debian packages will be required:

- libmariadb3 and libmariadb-dev, needed for MariaDB Python -connection. 
- LAMP stack packages. If you know what to do, you can use obviously anything else as a reverse proxy than Apache2. Apache2 should have following modules enabled: headers, rewrite, proxy, proxy_http with a2enmod for reverse proxy
- In some cases, the python3-wheel package has been required as well for MariaDB Python connection.

Debian 10 has been the only tested distribution with this project and seems to be working perfectly.

## Setup

## Flask-project initialization
After cloning this whole project, navigate to the thermoflask-server folder section.

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

With SQL shell execute following and remember to create a secure password for the user. It is required for the Flask-application to access the database in the ```config.py``` file you're going to create afterwards:

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

Create config.py based on config-sample.py. Generate your own API password to access the project with clients e.g. with openssl base64 -random utility and populate the MySQL section with your own credentials which you just created.

The freely selectable API password is configure on the line that says: ```api_pass``` and should be programmed later on all sensor units.

# Running (for development)

Generally run-server-dev.sh and run-server-prod.sh files contain necessary command line statements to run the project. However production mode should be done e.g. behind gunicorn. The native HTTP server is inefficient to this task and meant for development purposes only. The only difference with these two files is how much logs they generate in the shell.

# Configuring apache2 with gunicorn

Gunicorn is a a well performing "Python WSGI HTTP Server for UNIX". Configuring this project with gunicorn instead of using the native and inefficient Flask HTTP server is ideal and it works well with the Apache2.

Gunicorn is already installed at this point as a requirement specified in the requirements.txt and available for the virtual environment. It can be tested on the server directory by issuing e.g.:

```gunicorn --bind 127.0.0.1:5000 wsgi:app```

Remember to ensure you're not attempting to bind into a port already in use. You can test if this works e.g. by issuing:

```curl localhost:5000/records``` 

after which you should receive an intentional authentication failure message.

To make this into a service that does not need to be started manually, proceed to configuring systemd in the next section, and close the gunicorn server if it were open for testing.

Before that remember to make Apache2 already able to receive requests from such service.

``` 
ProxyPass /api http://127.0.0.1:5000
ProxyPassReverse /api http://127.0.0.1:5000
``` 

You can also test if this works by attempting to reach the service via public Internet.

# Systemd unit file creation

Creating this service file makes it possible to start this service automatically after network connectivity has been established on the server side.

This is an example file that can be put e.g. into ```/etc/systemd/system/thermoflask.service```

The service is intended to be ran by individual users and in this case, mpm_itk module of the Apache2 has been used for process isolation which is why the service is ran by thermoflask -user.

``` 
[Unit]
Description=Thermometer server with Flask
After=network.target

[Service]
User=thermoflask
Group=thermoflask
WorkingDirectory=FULLPATH_TO_THE_PROJECT
Environment="PATH=FULLPATH_TO_THE_PROJECT/venv/bin"
ExecStart=FULLPATH_TO_THE_PROJECT/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

It is also possible to bind into Unix sockets as well, but for e.g. Apache2 using it's proxy module this support is not well developed due to character limits on socket paths.

After creating this file, reload the systemd with

```systemctl daemon-reload```

and start the service by issuing:

```systemctl start thermoflask```

To check the status of the service, use the following command. If everything seems to be functioning properly, proceed to configuring the Apache2 as a reverse proxy.

```systemctl status thermoflask```

You could also test the functionality with curl by issuing:

```curl localhost:5000/records``` 

Which should create an intentional error of authentication failure.

The service should be now behing HTTP BASIC authentication, Apache2, Gunicorn with Flask finally serving inputs and outputs.