import json 
import numbers
import sys
import mariadb
from config import *

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        port=mysql_port,
        database=mysql_database,
        autocommit=True

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


#Sanity check for input data, check that we are actually processing just numbers and expected keys match to what we want to receive
def ThermalDataValidator(tempdata):
    expected_keys = ['temperature', 'humidity', 'timestamp']
    received_keys = []
    #Assuming data is valid
    sanity_state = True
    for key in tempdata:
        if key in expected_keys and isinstance(tempdata[key], numbers.Real): 
            pass
        else:
            sanity_state = False
        received_keys.append(key)
    #Additional check to see if match to what we expect to see
    #Sort and then compare
    expected_keys.sort()
    received_keys.sort()
    if expected_keys == received_keys:
        pass
    else:
        sanity_state = False
    return sanity_state


#Stores values into MariaDB/MySQL database, automatic commits are online and require no further actions
def Store_thermo_entry(device_id, temp, humidity,timestamp):
    sql = "INSERT INTO data_entries (device_id,temp,humidity,timestamp) VALUES ('{}','{}','{}','{}')".format(str(device_id), temp, humidity,timestamp)
    try:
        cur.execute(sql)
        #When commit is OK
        return True
    except Exception as e:
        #Error is logged into console or syslog depending on deployment, return false to tell about error in DB 
        print(f"Error: {e}")
        return False